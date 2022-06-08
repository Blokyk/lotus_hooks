from log_utils import dim, dim_warn, warn, write
from utils import run, print
from os.path import basename

def link_artifacts(actual_file: str, link_name: str):
    # since they are the same, we can just replace the old artifacts with a symlink
    # to the new one.
    if ((ln_result := run(["ln", "-sf", actual_file, link_name])).retcode != 0
        or (ln_result := run(["ln", "-sf", actual_file + ".png", link_name + ".png"])).retcode != 0):
        print("\t[bold][yellow]Δ", "[italic yellow]\[Couldn't relink old artifacts\]")
        print(ln_result.output)

def generate_error_artifacts(new_dot_path: str, prev_dot_path: str, compare_path: str):
    print("[bold yellow]If you want to see the images, run this command :")
    write(f"\tscp ubuntu@rpi:{new_dot_path}.png ~/ && xdg-open ~/{basename(new_dot_path)}.png")

    if (compare_result := run(["compare", prev_dot_path + ".png", new_dot_path + ".png", compare_path])).retcode != 0:
        dim_warn(f"Couldn't generate [white not dim]{basename(compare_path)}")
        dim("[dim](" + str(compare_result.retcode) + ") " + compare_result.output)

    print("If you want to see a visual diff of the images, run this command :")
    write(f"\tscp ubuntu@rpi:{compare_path} ~/ && xdg-open ~/{basename(compare_path)}")

def generate_artifacts(new_dot_path: str, prev_dot_path: str):
    print("MOCK: generating artifacts...")
