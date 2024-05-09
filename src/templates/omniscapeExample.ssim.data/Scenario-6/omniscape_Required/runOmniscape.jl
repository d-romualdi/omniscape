cd(raw"C:\gitprojects\omniscape\src\templates\omniscapeExample.ssim.data\Scenario-6\omniscape_Required")

using Pkg; Pkg.add(name="Omniscape", version="0.5.7")
using Omniscape
run_omniscape("config.ini")