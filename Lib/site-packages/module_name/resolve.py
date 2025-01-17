import os.path
import importlib


def gen_output(path, flag, debug=False):
    try:
        module_ns = get_module_name(path, debug)
    except Exception as e:
        if debug:
            print(str(e))
        module_ns = None

    if module_ns is None:
        return path
    if flag:
        return "-m " + module_ns
    return module_ns


def get_module_name(path, debug=False):
    orig_path = path
    path, fn = os.path.split(path)
    if not fn.endswith('.py'):
        if debug:
            print(path, 'is not python file')
        return None
    module_name = os.path.splitext(fn)[0]
    names = [module_name]

    while path:
        if not is_package(path):
            if debug:
                print(path, 'is not a package')
                print('names=', names)
            break
        path, name = path.rsplit(os.path.sep, 1)
        names.append(name)

    # means that file was not within a package
    if len(names) == 1:
        return None

    module_ns = '.'.join(reversed(names))
    root_package = names[-1]
    pkg_spec = importlib.util.find_spec(root_package)

    if pkg_spec is None:
        return None

    root_path = pkg_spec.submodule_search_locations[0]

    # instead of loading, we use simple heuristic. if root package
    # exists and in same location as orig_path, then we're good
    orig_path = os.path.realpath(orig_path)
    root_path = os.path.realpath(root_path)
    if orig_path.startswith(root_path):
        return module_ns
    return None


def is_package(path):
    init_file = os.path.join(path, '__init__.py')
    return os.path.isfile(init_file)
