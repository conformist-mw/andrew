def escape(string):
    string = str(string)
    return string.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
