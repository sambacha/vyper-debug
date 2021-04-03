from vyper.parser import parser
from vyper.parser.global_context import GlobalContext
from vyper.types import (
    ByteArrayType,
    get_size_of_type,
    MappingType,
    StringType,
    StructType,
    TupleType,
    ListType,
)
from vyper import compile_lll
from vyper import optimizer
from vyper.parser.parser import parse_to_lll


def serialise_var_rec(var_rec):
    if isinstance(var_rec.typ, ByteArrayType):
        type_str = "bytes[%s]" % var_rec.typ.maxlen
        _size = get_size_of_type(var_rec.typ) * 32
    elif isinstance(var_rec.typ, StringType):
        type_str = "string[%s]" % var_rec.typ.maxlen
        _size = get_size_of_type(var_rec.typ) * 32
    elif isinstance(var_rec.typ, StructType):
        type_str = "struct[%s]" % var_rec.typ.name
        _size = get_size_of_type(var_rec.typ) * 32
    elif isinstance(var_rec.typ, TupleType):
        type_str = "tuple"
        _size = get_size_of_type(var_rec.typ) * 32
    elif isinstance(var_rec.typ, ListType):
        type_str = str(var_rec.typ)
        _size = get_size_of_type(var_rec.typ) * 32
    elif isinstance(var_rec.typ, MappingType):
        type_str = str(var_rec.typ)
        _size = 0
    else:
        type_str = str(var_rec.typ)
        _size = get_size_of_type(var_rec.typ) * 32

    out = {"type": type_str, "size": _size, "position": var_rec.pos}
    return out


def produce_source_map(code, interface_codes=None):
    global_ctx = GlobalContext.get_global_context(
        parser.parse_to_ast(code), interface_codes=interface_codes
    )
    asm_list = compile_lll.compile_to_assembly(
        optimizer.optimize(
            parse_to_lll(code, runtime_only=True, interface_codes=interface_codes)
        )
    )
    c, line_number_map = compile_lll.assembly_to_evm(asm_list)
    source_map = {"globals": {}, "locals": {}, "line_number_map": line_number_map}
    source_map["globals"] = {
        name: serialise_var_rec(var_record)
        for name, var_record in global_ctx._globals.items()
    }
    # Fetch context for each function.
    lll = parser.parse_tree_to_lll(
        parser.parse_to_ast(code),
        code,
        interface_codes=interface_codes,
        runtime_only=True,
    )
    contexts = {f.func_name: f.context for f in lll.args[1:] if hasattr(f, "context")}

    prev_func_name = None
    for _def in global_ctx._defs:
        if _def.name != "__init__":
            func_info = {"from_lineno": _def.lineno, "variables": {}}
            # set local variables for specific function.
            context = contexts[_def.name]
            func_info["variables"] = {
                var_name: serialise_var_rec(var_rec)
                for var_name, var_rec in context.vars.items()
            }

            source_map["locals"][_def.name] = func_info
            # set to_lineno
            if prev_func_name:
                source_map["locals"][prev_func_name]["to_lineno"] = _def.lineno
            prev_func_name = _def.name

    source_map["locals"][_def.name]["to_lineno"] = len(code.splitlines())

    return source_map
