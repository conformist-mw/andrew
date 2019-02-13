def escape(string):
    return string.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
