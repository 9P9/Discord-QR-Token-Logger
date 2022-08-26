pystray_img = "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"

banner = """

 ██████╗ ██████╗       ██████╗ ██╗ ██████╗ █████╗  █████╗ ██████╗ ██████╗       ██╗      █████╗  ██████╗ ██╗███╗  ██╗
██╔═══██╗██╔══██╗      ██╔══██╗██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗      ██║     ██╔══██╗██╔════╝ ██║████╗ ██║
██║██╗██║██████╔╝█████╗██║  ██║██║╚█████╗ ██║  ╚═╝██║  ██║██████╔╝██║  ██║█████╗██║     ██║  ██║██║  ██╗ ██║██╔██╗██║
╚██████╔╝██╔══██╗╚════╝██║  ██║██║ ╚═══██╗██║  ██╗██║  ██║██╔══██╗██║  ██║╚════╝██║     ██║  ██║██║  ╚██╗██║██║╚████║
 ╚═██╔═╝ ██║  ██║      ██████╔╝██║██████╔╝╚█████╔╝╚█████╔╝██║  ██║██████╔╝      ███████╗╚█████╔╝╚██████╔╝██║██║ ╚███║
   ╚═╝   ╚═╝  ╚═╝      ╚═════╝ ╚═╝╚═════╝  ╚════╝  ╚════╝ ╚═╝  ╚═╝╚═════╝       ╚══════╝ ╚════╝  ╚═════╝ ╚═╝╚═╝  ╚══╝

"""