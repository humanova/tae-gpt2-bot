import codecs
import glob
import sys

# modify specific str in line
modifications = {
    "<|startoftext|>" : ""
}

def format_line(line):
    if "====================" in line:
        return "[null_line]"

    for k in modifications.keys():
        line = line.replace(k, modifications[k])
    return line


def merge(txt_dir, out_dir):
    txt_files = glob.glob(f"{txt_dir}/*.txt")

    print(txt_files)
    print(f"merging {','.join(txt_files)}")
    lines = ['']
    for f in txt_files:
        for line in codecs.open(f, "r", "utf-8").readlines():
            lines.append(format_line(line))
    # remove null lines
    for l in lines:
        if l == "[null_line]":
            lines.remove(l)
    # remove duplicates 
    lines = list(dict.fromkeys(lines))
    out_file = codecs.open("merge_out.txt", "w", "utf-8")
    out_file.writelines(lines)
    out_file.close()

if __name__ == "__main__":
    merge(sys.argv[1], sys.argv[2])
    print("finished merging")