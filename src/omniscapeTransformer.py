## omniscape

# Set up -----------------------------------------------------------------------

import pysyncrosim as ps
import pandas as pd
import sys
import os
import rasterio

ps.environment.progress_bar(message="Setting up Scenario", report_type="message")

e = ps.environment._environment()
wrkDir = e.data_directory.item() ## kb - changed from output directory to data dir

if os.path.exists(wrkDir) == False:
    os.mkdir(wrkDir)

myLibrary = ps.Library()
myScenarioID = e.scenario_id.item()
myScenario = myLibrary.scenarios(myScenarioID)
myScenarioParentID = int(myScenario.parent_id)
myParentScenario = myLibrary.scenarios(sid = myScenarioParentID)

dataPath = os.path.join(wrkDir, "Scenario-" + repr(myScenarioID)) 



# Load input and settings from SyncroSim Library ------------------------------- 

requiredData = myScenario.datasheets(name = "omniscape_Required")
requiredDataValidation = myScenario.datasheets(name = "omniscape_Required", show_full_paths=True)
generalOptions = myScenario.datasheets(name = "omniscape_GeneralOptions")
resistanceOptions = myScenario.datasheets(name = "omniscape_ResistanceOptions")
reclassTable = myScenario.datasheets(name = "omniscape_ReclassTable")
condition1 = myScenario.datasheets(name = "omniscape_Condition1")
condition2 = myScenario.datasheets(name = "omniscape_Condition2")
conditionalOptions = myScenario.datasheets(name = "omniscape_ConditionalOptions")
futureConditions = myScenario.datasheets(name = "omniscape_FutureConditions")
outputOptions = myScenario.datasheets(name = "omniscape_OutputOptions")
multiprocessing = myScenario.datasheets(name = "core_Multiprocessing")
juliaConfig = myScenario.datasheets(name = "omniscape_juliaConfiguration")



# If not provided, set default values  -----------------------------------------

if generalOptions.sourceFromResistance[0] == "Yes":
   requiredData.sourceFile = pd.Series("None")

if generalOptions.blockSize.empty:
    generalOptions.blockSize = pd.Series(1)

if generalOptions.sourceFromResistance[0] != generalOptions.sourceFromResistance[0]:
    generalOptions.sourceFromResistance = pd.Series("No")

if generalOptions.resistanceIsConductance[0] != generalOptions.resistanceIsConductance[0]:
    generalOptions.resistanceIsConductance = pd.Series("No")

if generalOptions.rCutoff[0] != generalOptions.rCutoff[0]:
    generalOptions.rCutoff = pd.Series("Inf")

if generalOptions.buffer[0] != generalOptions.buffer[0]:
    generalOptions.buffer = pd.Series(0)

if generalOptions.sourceThreshold[0] != generalOptions.sourceThreshold[0]:
    generalOptions.sourceThreshold = pd.Series(0)

if generalOptions.calcNormalizedCurrent[0] != generalOptions.calcNormalizedCurrent[0]:
    generalOptions.calcNormalizedCurrent = pd.Series("No")

if generalOptions.calcFlowPotential[0] != generalOptions.calcFlowPotential[0]:
    generalOptions.calcFlowPotential = pd.Series("No")

if generalOptions.allowDifferentProjections[0] != generalOptions.allowDifferentProjections[0]:
    generalOptions.allowDifferentProjections = pd.Series("No")

if generalOptions.connectFourNeighborsOnly[0] != generalOptions.connectFourNeighborsOnly[0]:
    generalOptions.connectFourNeighborsOnly = pd.Series("No")

if generalOptions.solver[0] != generalOptions.solver[0]:
    generalOptions.solver = pd.Series("cg+amg")

if resistanceOptions.reclassifyResistance.empty:
    resistanceOptions.reclassifyResistance = pd.Series("No")

if resistanceOptions.reclassifyResistance.item() == "No":
    resistanceOptions.reclassTable = pd.Series("None")

if resistanceOptions.writeReclassifiedResistance[0] != resistanceOptions.writeReclassifiedResistance[0]:
    resistanceOptions.writeReclassifiedResistance = pd.Series("Yes")

if conditionalOptions.conditional.empty:
    conditionalOptions.conditional = pd.Series("No")

if conditionalOptions.nConditions[0] != conditionalOptions.nConditions[0]:
    conditionalOptions.nConditions = pd.Series(1)

if conditionalOptions.conditional.item() == "No":
    condition1.condition1File = pd.Series("None")
    condition1.condition1Lower = pd.Series("NaN")
    condition1.condition1Upper = pd.Series("NaN")
    condition2.condition2File = pd.Series("None")
    condition2.condition2Lower = pd.Series("NaN")
    condition2.condition2Upper = pd.Series("NaN")

if condition1.comparison1[0] != condition1.comparison1[0]:
    condition1.comparison1 = pd.Series("within")

if condition2.comparison2[0] != condition2.comparison2[0]:
    condition2.comparison2 = pd.Series("within")

if futureConditions.compareToFuture.empty:
    futureConditions.compareToFuture = pd.Series("none")

if futureConditions.compareToFuture.item() == "none":
    futureConditions.condition1FutureFile = pd.Series("None")
    futureConditions.condition2FutureFile = pd.Series("None")

if outputOptions.writeRawCurrmap.empty:
    outputOptions.writeRawCurrmap = pd.Series("Yes")

if outputOptions.maskNodata[0] != outputOptions.maskNodata[0]:
    outputOptions.maskNodata = pd.Series("Yes")

if outputOptions.writeAsTif[0] != outputOptions.writeAsTif[0]:
    outputOptions.writeAsTif = pd.Series("Yes")



# Validation -------------------------------------------------------------------

if juliaConfig.juliaPath.empty:
    sys.exit("A julia executable is required.")

if not os.path.isfile(juliaConfig.juliaPath[0]):
    sys.exit("The path to the julia executable is not valid or does not exist.")

if ' ' in juliaConfig.juliaPath[0]:
    sys.exit("The path to the julia executable may not contains spaces.")

if not 'julia.exe' in juliaConfig.juliaPath[0]:
    sys.exit("The path to the julia executable must contain the 'julia.exe' file.")

if requiredData.resistanceFile[0] != requiredData.resistanceFile[0]:
    sys.exit("'Resistance file' is required.")

if requiredData.radius[0] != requiredData.radius[0]:
    sys.exit("'Radius' is required.")

if generalOptions.sourceFromResistance[0] == "No" and requiredData.sourceFile[0] == "None":
    sys.exit("'Source from resistance' was set to 'No', therefore 'Source file' is required.")

if generalOptions.sourceFromResistance[0] == "No" and requiredDataValidation.sourceFile[0] == requiredDataValidation.sourceFile[0]:
    resistanceLayer = rasterio.open(requiredDataValidation.resistanceFile[0])
    sourceLayer = rasterio.open(requiredDataValidation.sourceFile[0])
    if resistanceLayer.crs != sourceLayer.crs:
        sys.exit("'Resistance file' and 'Source file' must have the same Coordinate Reference System.")
    if resistanceLayer.bounds != sourceLayer.bounds:
        sys.exit("'Resistance file' and 'Source file' must have the same raster extent.")

if not resistanceOptions.empty:
    if resistanceOptions.reclassifyResistance[0] == "Yes":
        if reclassTable.empty:
            sys.exit("'Reclassify resistance' was set to 'Yes', therefore 'Reclass Table' is required.")
        if reclassTable['landCover'].isnull().values.any():
            sys.exit("'Reclass Table' has NaN values for 'Land cover class'.")
        if reclassTable['resistanceValue'].isnull().values.any():
            sys.exit("'Reclass Table' has NaN values for 'Resistance value'. If necessary, NaN values should be specified as -9999.")
    
if not conditionalOptions.empty:
    if conditionalOptions.conditional[0] == "Yes" and conditionalOptions.nConditions[0] == "1" and condition1.condition1File[0] != condition1.condition1File[0]:
        sys.exit("'Conditional' was set to 'Yes' and 'Number of conditions' was set to 1, therefore 'Condition 1 file' is required.")
    if conditionalOptions.conditional[0] == "Yes" and conditionalOptions.nConditions[0] == 2 and (condition1.condition1File[0] != condition1.condition1File[0] or condition2.condition2File[0] != condition2.condition2File[0]):
        sys.exit("'Conditional' was set to 'Yes' and 'Number of conditions' was set to 2, therefore 'Condition 1 file' and 'Condition 2 file' are required.")
    if condition1.comparison1[0] == "within" and (condition1.condition1Lower[0] != condition1.condition1Lower[0] or condition1.condition1Upper[0] != condition1.condition1Upper[0]):
        sys.exit("'Comparison 1' was set to 'within', therefore 'Condition 1 lower' and 'Condition 1 upper' are required.")
    if condition2.comparison2[0] == "within" and (condition2.condition2Lower[0] != condition2.condition2Lower[0] or condition2.condition2Upper[0] != condition2.condition2Upper[0]):
        sys.exit("'Comparison 2' was set to 'within', therefore 'Condition 2 lower' and 'Condition 2 upper' are required.")

if not futureConditions.empty:
    if futureConditions.compareToFuture[0] == "1" and futureConditions.condition1FutureFile[0] != futureConditions.condition1FutureFile[0]:
        sys.exit("'Compare to future' was set to 1, therefore 'Condition 1 future file' is required.")
    if futureConditions.compareToFuture[0] == "2" and futureConditions.condition2FutureFile[0] != futureConditions.condition2FutureFile[0]:
        sys.exit("'Compare to future' was set to 2, therefore 'Condition 2 future file' is required.")
    if futureConditions.compareToFuture[0] == "both" and (futureConditions.condition1FutureFile[0] != futureConditions.condition1FutureFile[0] or futureConditions.condition2FutureFile[0] != futureConditions.condition2FutureFile[0]):
        sys.exit("'Compare to future' was set to 'both', therefore 'Condition 1 future file' and 'Condition 2 future file' are required.")



# Change "Yes" and "No" to "true" and "false" ----------------------------------

generalOptions = generalOptions.replace({'Yes': 'true', 'No': 'false'})
resistanceOptions = resistanceOptions.replace({'Yes': 'true', 'No': 'false'})
conditionalOptions = conditionalOptions.replace({'Yes': 'true', 'No': 'false'})
outputOptions = outputOptions.replace({'Yes': 'true', 'No': 'false'})
multiprocessing = multiprocessing.replace({'Yes': 'true', 'No': 'false'})



# Prepare reclass file ---------------------------------------------------------

if not reclassTable.empty:
    reclassTablePath = os.path.join(dataPath, "omniscape_ResistanceOptions")
    if os.path.exists(reclassTablePath) == False:
        os.mkdir(reclassTablePath)
    reclassTable.loc[reclassTable["resistanceValue"] == -9999, "resistanceValue"] = "missing"
    with open(os.path.join(reclassTablePath, "reclass_table.txt"), "w") as f:
        file = reclassTable.to_string(header=False, index=False)
        f.write(file)
else:
    reclassTablePath = "None"

# Prepare configuration file (.ini) --------------------------------------------

file = open(os.path.join(dataPath, "omniscape_Required", "config.ini"), "w")
file.write(
    "[Required]" + "\n"
    "resistance_file = " + os.path.join(dataPath, "omniscape_Required", requiredData.resistanceFile[0]) + "\n"
    "radius = " + repr(requiredData.radius[0]) + "\n"
    "project_name = " + os.path.join(wrkDir, "Scenario-" + repr(myScenarioID), "omniscape_outputSpatial") + "\n"
    "source_file = " + requiredData.sourceFile[0] + "\n"
    "\n"
    "[General Options]" + "\n"
    "block_size = " + repr(generalOptions.blockSize[0]) + "\n"
    "source_from_resistance = " + generalOptions.sourceFromResistance[0] + "\n"
    "resistance_is_conductance = " + generalOptions.resistanceIsConductance[0] + "\n"
    "r_cutoff = 1" + "\n"
    "buffer = " + repr(generalOptions.buffer[0]) + "\n"
    "source_threshold = " + repr(generalOptions.sourceThreshold[0]) + "\n"
    "calc_normalized_current = " + generalOptions.calcNormalizedCurrent[0] + "\n"
    "calc_flow_potential = " + generalOptions.calcFlowPotential[0] + "\n"
    "allow_different_projections = " + generalOptions.allowDifferentProjections[0] + "\n"
    "connect_four_neighbors_only = " + generalOptions.connectFourNeighborsOnly[0] + "\n"
    "solver = " + generalOptions.solver[0] + "\n"
    "\n"
    "[Resistance Reclassification]" + "\n"
    "reclassify_resistance = " + resistanceOptions.reclassifyResistance[0] + "\n"
    "reclass_table = " + os.path.join(reclassTablePath, "reclass_table.txt") + "\n"
    "write_reclassified_resistance = " + resistanceOptions.writeReclassifiedResistance[0] + "\n"
    "\n"
    "[Conditional Connectivity]" + "\n"
    "conditional = " + conditionalOptions.conditional[0] + "\n"
    "n_conditions = " + repr(conditionalOptions.nConditions[0]) + "\n"
    "condition1_file = " + condition1.condition1File[0] + "\n"
    "comparison1 = " + condition1.comparison1[0] + "\n"
    "condition1_lower = " + condition1.condition1Lower[0] + "\n"
    "condition1_upper = " + condition1.condition1Upper[0] + "\n"
    "condition2_file = " + condition2.condition2File[0] + "\n"
    "comparison2 = " + condition2.comparison2[0] + "\n"
    "condition2_lower = " + condition2.condition2Lower[0] + "\n"
    "condition2_upper = " + condition2.condition2Upper[0] + "\n"
    "compare_to_future = " + futureConditions.compareToFuture[0] + "\n"
    "condition1_future_file = " + futureConditions.condition1FutureFile[0] + "\n"
    "condition2_future_file = " + futureConditions.condition2FutureFile[0] + "\n"
    "\n"
    "[Output Options]" + "\n"
    "write_raw_currmap = " + outputOptions.writeRawCurrmap[0] + "\n"
    "mask_nodata = " + outputOptions.maskNodata[0] + "\n"
    "write_as_tif = " + outputOptions.writeAsTif[0] + "\n"
    "\n"
    "[Multiprocessing]" + "\n"
    "parallelize = " + multiprocessing.EnableMultiprocessing[0] + "\n"
    "parallel_batch_size = " + repr(multiprocessing.MaximumJobs[0]) + "\n"
)
file.close()



# Prepare julia script ---------------------------------------------------------

configName = "config.ini"

file = open(os.path.join(dataPath, "omniscape_Required", "runOmniscape.jl"), "w")
file.write(
    "cd(raw\"" + os.path.join(dataPath, "omniscape_Required") + "\")" + "\n"
    "\n"
    "using Pkg; Pkg.add(name=\"Omniscape\", version=\"0.5.7\")" + "\n"
    "using Omniscape" + "\n"
    "run_omniscape(\"" + configName + "\")"
)
file.close()



# Run julia script with system call -------------------------------------------------------------

ps.environment.progress_bar(message="Running Omniscape", report_type="message")

jlExe = juliaConfig.juliaPath[0]
runFile = os.path.join(dataPath, "omniscape_Required", "runOmniscape.jl")

if ' ' in dataPath:
    sys.exit("Due to julia requirements, the path to the SyncroSim Library may not contain any spaces.")

runOmniscape = jlExe + " " + runFile

os.system(runOmniscape)



# Create output datasheets ----------------------------------------------------------------------

myOutput = myScenario.datasheets(name = "omniscape_outputSpatial")

if outputOptions.writeRawCurrmap[0] == "true":
    myOutput.cumCurrmap = pd.Series(os.path.join(wrkDir, "Scenario-" + repr(myScenarioID), "omniscape_outputSpatial", "cum_currmap.tif"))

if generalOptions.calcFlowPotential[0] == "true":
    myOutput.flowPotential = pd.Series(os.path.join(wrkDir, "Scenario-" + repr(myScenarioID), "omniscape_outputSpatial", "flow_potential.tif"))

if generalOptions.calcNormalizedCurrent[0] == "true":
    myOutput.normalizedCumCurrmap = pd.Series(os.path.join(wrkDir, "Scenario-" + repr(myScenarioID), "omniscape_outputSpatial", "normalized_cum_currmap.tif"))

if (os.path.isfile(os.path.join(wrkDir, "Scenario-" + repr(myScenarioID), "omniscape_outputSpatial", "classified_resistance.tif"))) & (resistanceOptions.writeReclassifiedResistance[0] == "true"):
    myOutput.classifiedResistance = pd.Series(os.path.join(wrkDir, "Scenario-" + repr(myScenarioID), "omniscape_outputSpatial", "classified_resistance.tif"))
else:
    myOutput.classifiedResistance = pd.Series(requiredDataValidation.resistanceFile[0])



# Save outputs to SyncroSim ---------------------------------------------------------------------

myParentScenario.save_datasheet(name = "omniscape_outputSpatial", data = myOutput)


