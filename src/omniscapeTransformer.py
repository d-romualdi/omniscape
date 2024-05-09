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

if generalOptions.source_from_resistance[0] == "Yes":
   requiredData.source_file = pd.Series("None")

if generalOptions.block_size.empty:
    generalOptions.block_size = pd.Series(1)

if generalOptions.source_from_resistance[0] != generalOptions.source_from_resistance[0]:
    generalOptions.source_from_resistance = pd.Series("No")

if generalOptions.resistance_is_conductance[0] != generalOptions.resistance_is_conductance[0]:
    generalOptions.resistance_is_conductance = pd.Series("No")

if generalOptions.r_cutoff[0] != generalOptions.r_cutoff[0]:
    generalOptions.r_cutoff = pd.Series("Inf")

if generalOptions.buffer[0] != generalOptions.buffer[0]:
    generalOptions.buffer = pd.Series(0)

if generalOptions.source_threshold[0] != generalOptions.source_threshold[0]:
    generalOptions.source_threshold = pd.Series(0)

if generalOptions.calc_normalized_current[0] != generalOptions.calc_normalized_current[0]:
    generalOptions.calc_normalized_current = pd.Series("No")

if generalOptions.calc_flow_potential[0] != generalOptions.calc_flow_potential[0]:
    generalOptions.calc_flow_potential = pd.Series("No")

if generalOptions.allow_different_projections[0] != generalOptions.allow_different_projections[0]:
    generalOptions.allow_different_projections = pd.Series("No")

if generalOptions.connect_four_neighbors_only[0] != generalOptions.connect_four_neighbors_only[0]:
    generalOptions.connect_four_neighbors_only = pd.Series("No")

if generalOptions.solver[0] != generalOptions.solver[0]:
    generalOptions.solver = pd.Series("cg+amg")

if resistanceOptions.reclassify_resistance.empty:
    resistanceOptions.reclassify_resistance = pd.Series("No")

if resistanceOptions.reclassify_resistance.item() == "No":
    resistanceOptions.reclass_table = pd.Series("None")

if resistanceOptions.write_reclassified_resistance[0] != resistanceOptions.write_reclassified_resistance[0]:
    resistanceOptions.write_reclassified_resistance = pd.Series("Yes")

if conditionalOptions.conditional.empty:
    conditionalOptions.conditional = pd.Series("No")

if conditionalOptions.n_conditions[0] != conditionalOptions.n_conditions[0]:
    conditionalOptions.n_conditions = pd.Series(1)

if conditionalOptions.conditional.item() == "No":
    condition1.condition1_file = pd.Series("None")
    condition1.condition1_lower = pd.Series("NaN")
    condition1.condition1_upper = pd.Series("NaN")
    condition2.condition2_file = pd.Series("None")
    condition2.condition2_lower = pd.Series("NaN")
    condition2.condition2_upper = pd.Series("NaN")

if condition1.comparison1[0] != condition1.comparison1[0]:
    condition1.comparison1 = pd.Series("within")

if condition2.comparison2[0] != condition2.comparison2[0]:
    condition2.comparison2 = pd.Series("within")

if futureConditions.compare_to_future.empty:
    futureConditions.compare_to_future = pd.Series("none")

if futureConditions.compare_to_future.item() == "none":
    futureConditions.condition1_future_file = pd.Series("None")
    futureConditions.condition2_future_file = pd.Series("None")

if outputOptions.write_raw_currmap.empty:
    outputOptions.write_raw_currmap = pd.Series("Yes")

if outputOptions.mask_nodata[0] != outputOptions.mask_nodata[0]:
    outputOptions.mask_nodata = pd.Series("Yes")

if outputOptions.write_as_tif[0] != outputOptions.write_as_tif[0]:
    outputOptions.write_as_tif = pd.Series("Yes")



# Validation -------------------------------------------------------------------

if juliaConfig.julia_path.empty:
    sys.exit("A julia executable is required.")

if not os.path.isfile(juliaConfig.julia_path[0]):
    sys.exit("The path to the julia executable is not valid or does not exist.")

if ' ' in juliaConfig.julia_path[0]:
    sys.exit("The path to the julia executable may not contains spaces.")

if not 'julia.exe' in juliaConfig.julia_path[0]:
    sys.exit("The path to the julia executable must contain the 'julia.exe' file.")

if requiredData.resistance_file[0] != requiredData.resistance_file[0]:
    sys.exit("'Resistance file' is required.")

if requiredData.radius[0] != requiredData.radius[0]:
    sys.exit("'Radius' is required.")

if generalOptions.source_from_resistance[0] == "No" and requiredData.source_file[0] == "None":
    sys.exit("'Source from resistance' was set to 'No', therefore 'Source file' is required.")

if generalOptions.source_from_resistance[0] == "No" and requiredDataValidation.source_file[0] == requiredDataValidation.source_file[0]:
    resistanceLayer = rasterio.open(requiredDataValidation.resistance_file[0])
    sourceLayer = rasterio.open(requiredDataValidation.source_file[0])
    if resistanceLayer.crs != sourceLayer.crs:
        sys.exit("'Resistance file' and 'Source file' must have the same Coordinate Reference System.")
    if resistanceLayer.bounds != sourceLayer.bounds:
        sys.exit("'Resistance file' and 'Source file' must have the same raster extent.")

if not resistanceOptions.empty:
    if resistanceOptions.reclassify_resistance[0] == "Yes":
        if reclassTable.empty:
            sys.exit("'Reclassify resistance' was set to 'Yes', therefore 'Reclass Table' is required.")
        if reclassTable['land_cover'].isnull().values.any():
            sys.exit("'Reclass Table' has NaN values for 'Land cover class'.")
        if reclassTable['resistance_value'].isnull().values.any():
            sys.exit("'Reclass Table' has NaN values for 'Resistance value'. If necessary, NaN values should be specified as -9999.")
    
if not conditionalOptions.empty:
    if conditionalOptions.conditional[0] == "Yes" and conditionalOptions.n_conditions[0] == "1" and condition1.condition1_file[0] != condition1.condition1_file[0]:
        sys.exit("'Conditional' was set to 'Yes' and 'Number of conditions' was set to 1, therefore 'Condition 1 file' is required.")
    if conditionalOptions.conditional[0] == "Yes" and conditionalOptions.n_conditions[0] == 2 and (condition1.condition1_file[0] != condition1.condition1_file[0] or condition2.condition2_file[0] != condition2.condition2_file[0]):
        sys.exit("'Conditional' was set to 'Yes' and 'Number of conditions' was set to 2, therefore 'Condition 1 file' and 'Condition 2 file' are required.")
    if condition1.comparison1[0] == "within" and (condition1.condition1_lower[0] != condition1.condition1_lower[0] or condition1.condition1_upper[0] != condition1.condition1_upper[0]):
        sys.exit("'Comparison 1' was set to 'within', therefore 'Condition 1 lower' and 'Condition 1 upper' are required.")
    if condition2.comparison2[0] == "within" and (condition2.condition2_lower[0] != condition2.condition2_lower[0] or condition2.condition2_upper[0] != condition2.condition2_upper[0]):
        sys.exit("'Comparison 2' was set to 'within', therefore 'Condition 2 lower' and 'Condition 2 upper' are required.")

if not futureConditions.empty:
    if futureConditions.compare_to_future[0] == "1" and futureConditions.condition1_future_file[0] != futureConditions.condition1_future_file[0]:
        sys.exit("'Compare to future' was set to 1, therefore 'Condition 1 future file' is required.")
    if futureConditions.compare_to_future[0] == "2" and futureConditions.condition2_future_file[0] != futureConditions.condition2_future_file[0]:
        sys.exit("'Compare to future' was set to 2, therefore 'Condition 2 future file' is required.")
    if futureConditions.compare_to_future[0] == "both" and (futureConditions.condition1_future_file[0] != futureConditions.condition1_future_file[0] or futureConditions.condition2_future_file[0] != futureConditions.condition2_future_file[0]):
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
    reclassTable.loc[reclassTable["resistance_value"] == -9999, "resistance_value"] = "missing"
    with open(os.path.join(reclassTablePath, "reclass_table.txt"), "w") as f:
        file = reclassTable.to_string(header=False, index=False)
        f.write(file)
else:
    reclassTablePath = "None"

# Prepare configuration file (.ini) --------------------------------------------

file = open(os.path.join(dataPath, "omniscape_Required", "config.ini"), "w")
file.write(
    "[Required]" + "\n"
    "resistance_file = " + os.path.join(dataPath, "omniscape_Required", requiredData.resistance_file[0]) + "\n"
    "radius = " + repr(requiredData.radius[0]) + "\n"
    "project_name = " + os.path.join(wrkDir, "Scenario-" + repr(myScenarioID), "omniscape_outputSpatial") + "\n"
    "source_file = " + requiredData.source_file[0] + "\n"
    "\n"
    "[General Options]" + "\n"
    "block_size = " + repr(generalOptions.block_size[0]) + "\n"
    "source_from_resistance = " + generalOptions.source_from_resistance[0] + "\n"
    "resistance_is_conductance = " + generalOptions.resistance_is_conductance[0] + "\n"
    "r_cutoff = 1" + "\n"
    "buffer = " + repr(generalOptions.buffer[0]) + "\n"
    "source_threshold = " + repr(generalOptions.source_threshold[0]) + "\n"
    "calc_normalized_current = " + generalOptions.calc_normalized_current[0] + "\n"
    "calc_flow_potential = " + generalOptions.calc_flow_potential[0] + "\n"
    "allow_different_projections = " + generalOptions.allow_different_projections[0] + "\n"
    "connect_four_neighbors_only = " + generalOptions.connect_four_neighbors_only[0] + "\n"
    "solver = " + generalOptions.solver[0] + "\n"
    "\n"
    "[Resistance Reclassification]" + "\n"
    "reclassify_resistance = " + resistanceOptions.reclassify_resistance[0] + "\n"
    "reclass_table = " + os.path.join(reclassTablePath, "reclass_table.txt") + "\n"
    "write_reclassified_resistance = " + resistanceOptions.write_reclassified_resistance[0] + "\n"
    "\n"
    "[Conditional Connectivity]" + "\n"
    "conditional = " + conditionalOptions.conditional[0] + "\n"
    "n_conditions = " + repr(conditionalOptions.n_conditions[0]) + "\n"
    "condition1_file = " + condition1.condition1_file[0] + "\n"
    "comparison1 = " + condition1.comparison1[0] + "\n"
    "condition1_lower = " + condition1.condition1_lower[0] + "\n"
    "condition1_upper = " + condition1.condition1_upper[0] + "\n"
    "condition2_file = " + condition2.condition2_file[0] + "\n"
    "comparison2 = " + condition2.comparison2[0] + "\n"
    "condition2_lower = " + condition2.condition2_lower[0] + "\n"
    "condition2_upper = " + condition2.condition2_upper[0] + "\n"
    "compare_to_future = " + futureConditions.compare_to_future[0] + "\n"
    "condition1_future_file = " + futureConditions.condition1_future_file[0] + "\n"
    "condition2_future_file = " + futureConditions.condition2_future_file[0] + "\n"
    "\n"
    "[Output Options]" + "\n"
    "write_raw_currmap = " + outputOptions.write_raw_currmap[0] + "\n"
    "mask_nodata = " + outputOptions.mask_nodata[0] + "\n"
    "write_as_tif = " + outputOptions.write_as_tif[0] + "\n"
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

jlExe = juliaConfig.julia_path[0]
runFile = os.path.join(dataPath, "omniscape_Required", "runOmniscape.jl")

if ' ' in dataPath:
    sys.exit("Due to julia requirements, the path to the SyncroSim Library may not contain any spaces.")

runOmniscape = jlExe + " " + runFile

os.system(runOmniscape)



# Create output datasheets ----------------------------------------------------------------------

myOutput = myScenario.datasheets(name = "omniscape_outputSpatial")

if outputOptions.write_raw_currmap[0] == "true":
    myOutput.cum_currmap = pd.Series(os.path.join(wrkDir, "Scenario-" + repr(myScenarioID), "omniscape_outputSpatial", "cum_currmap.tif"))

if generalOptions.calc_flow_potential[0] == "true":
    myOutput.flow_potential = pd.Series(os.path.join(wrkDir, "Scenario-" + repr(myScenarioID), "omniscape_outputSpatial", "flow_potential.tif"))

if generalOptions.calc_normalized_current[0] == "true":
    myOutput.normalized_cum_currmap = pd.Series(os.path.join(wrkDir, "Scenario-" + repr(myScenarioID), "omniscape_outputSpatial", "normalized_cum_currmap.tif"))

if (os.path.isfile(os.path.join(wrkDir, "Scenario-" + repr(myScenarioID), "omniscape_outputSpatial", "classified_resistance.tif"))) & (resistanceOptions.write_reclassified_resistance[0] == "true"):
    myOutput.classified_resistance = pd.Series(os.path.join(wrkDir, "Scenario-" + repr(myScenarioID), "omniscape_outputSpatial", "classified_resistance.tif"))
else:
    myOutput.classified_resistance = pd.Series(requiredDataValidation.resistance_file[0])



# Save outputs to SyncroSim ---------------------------------------------------------------------

myParentScenario.save_datasheet(name = "omniscape_outputSpatial", data = myOutput)


