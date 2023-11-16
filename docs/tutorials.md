---
layout: default
title: Tutorials
permalink: /tutorials
---

## **Reproducing the Omniscape.jl example with omniscape SyncroSim**

This tutorial provides an overview of working with omniscape SyncroSim in the Windows user interface. It covers the following steps:
<A href="#step-1.-creating-and-configuring-an-omniscape-syncrosim-library">Step 1. Creating and configuring an omniscape SyncroSim Library</A>
<A href="#step-2.-visualizing-scenario-results">Step 2. Visualizing scenario results</A>
<A href="#step-3.-creating,-editing,-and-running-a-new-scenario">Step 3. Creating, editing, and running a new scenario</A>
<A href="#step 4.-comparing-results-across-scenarios">Step 4. Comparing results across scenarios</A>

<br>

_**Step 1. Creating and configuring an omniscape SyncroSim Library**_
In SyncroSim, a library is a file with extension .ssim that stores all the model’s inputs and outputs in a format specific to a given package. To create a new library:
1.	Open SyncroSim Desktop.
2.	Select **File > New**.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot6.png">

  a.	From the list of packages, select **omniscape**. Three template library options will be available: Empty Library, Omniscape Example, and Omniscape Impact.
  b.	Select the **Omniscape Example** template library. If desired, you may edit the *File name*, and change the *Folder* by clicking on the *Browse* button. Click **OK**.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot7.png">

A new library has been created based on the selected template. SyncroSim will automatically open and display it in the Library Explorer window.
3.	Double-click on the library name, **Omniscape Example**, to open the library properties window. You may also right-click on the library name and select **Properties** from the context menu.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot8.png">

4.	The *Summary* datasheet contains the metadata for the library.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot9.png">

5.	Navigate to the **Julia Configuration tab**.
The path to the **Julia executable** file must be specified to run **omniscape** SyncroSim. To do so, click on the folder icon and navigate to where Julia is installed in your computer. Its default location is **C:\Users\[User_Name]\AppData\Local\Programs\Julia-[version]\bin\julia.exe**. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot10.png">

> **Note:** The AppData folder is sometimes hidden. To see it, in File Explorer, select View > Show > Hidden items.

6.	Next, navigate to the **Options** tab. 
In the *General* datasheet, mark the checkbox for **Use conda**.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot11.png">

7.	Close the library properties window.

Next, you will review the inputs of the *Reference resistance* scenario. In SyncroSim, each scenario contains the model inputs and outputs associated with a model run.
1.	In the Library Explorer window, select the pre-configured scenario **Reference resistance** and double-click it to open its properties. You may also right-click on the scenario name and select **Properties** from the context menu.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot12.png">

2.	Navigate to the **Pipeline** datasheet.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot13.png">

  a.	Under the Stage column, note that two pipeline stages are set in the following order:
    i.	*Omniscape* – runs Omniscape.jl 
    ii.	*Categorize Connectivity Output* – classifies the continuous output from Omniscape.jl into connectivity categories based on a set of threshold values
Each pipeline stage calls on a transformer (*i.e.*, script) which takes the inputs from SyncroSim, runs a model, and returns the results to SyncroSim.

The *Omniscape* pipeline stage replicates the exact structure and order of parameters as Omniscape.jl with inputs organized in two tabs: *Required* and *Optional*. 
3.	Navigate to the **Required** tab, which contains the following inputs:
  a.	*Resistance file* – a raster file of land cover or resistance classes. For this example, the pre-loaded raster corresponds to the 2016 National Land Cover Dataset for central Maryland.
  b.	*Radius* – sets the radius of the moving window. This example uses a radius of 100 pixels.
  c.	*Source file* – a raster file indicating which pixels correspond to sources. In this example, the sources are set through a different method, described in the next step.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot14.png">

4.	Navigate to the **Optional** tab.
  a.	Under the *General Options* datasheet, note that *Source from resistance* is set to *Yes*, enforcing that the sources be calculated from the resistance layer based on a threshold of 1 as defined by *R cutoff*.
  
<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot15.png">

  b.	Navigate to the **Resistance Reclassification** node and review the following inputs:
    i.	*Options > Reclassify resistance* – determines whether the *Resistance file* should be reclassified. For this example, it is set to *Yes* since the *Resistance file* provided in step 11.a corresponded to a raster of land cover classes.
    ii.	*Options > Write reclassified resistance* – determines whether the reclassified resistance raster should be saved and written to file. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot16.png">

  iii.	*Reclass table* – a reclassification matrix used to translate land cover classes into resistance values.
    
<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot17.png">

The *Categorize Connectivity Output* pipeline stage is an exclusive feature of the **omniscape** SyncroSim package. It allows for seamless post-processing of the continuous output of Omniscape into discrete connectivity categories based on user-defined connectivity categories, a common step in the Omniscape workflow.
5.	In the Library Explorer, double-click on **Definitions** to open the project properties. You may also right-click on the project name and select **Properties** from the context menu. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot18.png">

6.	Under the *Summary* datasheet, the *Description* field highlights that the connectivity categories and thresholds used in the template library were derived from Cameron *et al.* (2022, Conservation Science and Practice).
7.	Navigate to the **Connectivity Categories** tab.
  a.	Note that four connectivity categories have been defined, each associated with an ID value.
  b.	Click on the **Category ID** column to sort categories in ascending order, where *Impeded* represents areas with the least amount of flow, and *Channelized* represents areas with the greatest amount to flow.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot19.png">

8.	Return to the scenario properties window, navigate to the **Advanced** tab.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot20.png">

Note that each connectivity category is associated with a minimum and maximum value, defining the range of normalized current flow that will be reclassified into each connectivity category.
9.	Close the scenario properties window.

_**Step 2. Visualizing scenario results**_
The Omniscape Example template library already contains the results for the *Reference resistance* scenario. In SyncroSim, the results for a scenario are organized into a *Results* folder, nested within its parent scenario. 
1.	In the Library Explorer window, click on the arrow beside the *Reference resistance* scenario to expose the *Results* folder; repeat the same action to expose the results scenario. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot21.png">

2.	Double-click on the results scenario to open its properties.
  a.	Click through the **Required**, **Optional** and **Advanced** tabs and note that the results scenario is a copy of the parent scenario’s inputs, which are greyed out. 
  
  <img align="left" style="padding: 13px" width="180" src="assets/images/screenshot22.png">
  
  b.	Navigate to the **Results** tab, which lists the spatial and tabular outputs. Both pipeline stages have spatial outputs but only the second pipeline stage has tabular outputs.
    i.	Under the **Spatial** node, the outputs from the first and second transformers are organized under the *Omniscape Outputs* and *Connectivity Categories* datasheets, respectively.
    You can export any spatial output by clicking on the *Export* button.
    
  <img align="left" style="padding: 13px" width="180" src="assets/images/screenshot23.png">
  
  ii.	Under the **Tabular** node, the output of the second transformer is saved to the *Connectivity Categories Summary* datasheet.
  You can export the tabular output by right-clicking on the data and selecting *Export All* from the context menu.
  
<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot24.png">

3.	Close the results scenario properties.

Using the SyncroSim built-in tools, you will now visualize the outputs of the first transformer.
4.	In the Library Explorer window, right-click on the **Reference resistance** scenario and select **Add to Results** from the context menu. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot25.png">

5.	Navigate to the **Maps** tab and double-click on the first pre-configured map, **Cumulative current flow**. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot26.png">

The cumulative current flow represents the total current flowing through the landscape. To inspect the map, consider the following:
  a.	*Map legend* – displayed along the left-hand side of the window. It can be edited by double-clicking it.
  b.	*Toolbar* – displayed along the top of the window. Includes zoom, pan and per pixel information tooltip.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot27.png">

6.	Close the map window and view the two following maps.
  a.	**Flow potential** represents current flow under the null condition of resistance set to 1 for the entire landscape. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot28.png">

  b.	**Normalized current flow** is calculated as flow potential divided by cumulative current, and therefore represents where there is more or less current than expected under null resistance conditions.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot29.png">

Next, you will visualize the outputs of the second transformer, which takes the *Normalized current flow* map and reclassifies it into a discrete map, based on the threshold values reviewed in steps 13-17.
7.	View the **Connectivity categories** map.
8.	Keep the map open for comparison and from the Library Explorer window, navigate to the **Charts** tab and view the **Area** chart. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot30.png">

Note that it summarized the amount of area per connectivity category.
Alternatively, a **Percent cover** summary is also available.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot31.png">

9.	Close all plot windows.

_**Step 3. Creating, editing, and running a new scenario**_
Next, you will learn how to create a scenario and run it to generate results. This scenario will differ from the *Reference resistance* by a ten-fold increase in resistance for all non-forest (i.e., non-source) pixels. 
1.	Right-click on the existing scenario and select **Copy** from the context menu. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot32.png">

Then, right-click anywhere inside the Library Explorer window and select **Paste**.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot33.png">

2.	Double-click on the new scenario to open its properties.
  a.	Change the **Name** to *Increased resistance*. 
  b.	Change the **Description** to *Resistance values for non-forest land cover types were increased by one order of magnitude. All other configuration options for Omniscape are equal to those implemented in the Omniscape.jl example*.
  
<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot34.png">

3.	Navigate to the **Optional** tab and under the **Resistance Reclassification** node, open the **Reclass table** datasheet.
  a.	Under the **Resistance value** column, increase values by one order of magnitude, except for *Land cover class* 41, 42, and 43, which represent forest classes.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot35.png">

4.	Close the scenario properties window and save the changes to the library.

Next, you will run the scenario. For this example, the run should take approximately 5 minutes with multiprocessing enabled across 5 cores.
5.	To enable multiprocessing, click on the **Multiprocessing** button along the SyncroSim toolbar and adjust the number of **Multiprocessing jobs** to 5.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot36.png">

6.	In the Library Explorer window, right-click on the **Increased resistance** scenario and select **Run** for the context menu.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot37.png">

  a.	The Run Monitor window will open, informing that the model is Running.
  
<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot38.png">

  b.	Along the bottom-right of the window, a progress bar will provide further details.
  c.	First, SyncroSim calls the first transformer, *Omniscape*. 
    i.	*Setting up Scenario* – the transformer takes the inputs and pre-processes them into the format required by Julia. 
    ii.	*Running Omniscape* – the transformer calls Julia to run the analysis. Once the analysis is complete, the transformer retrieves and saves the outputs back to SyncroSim. 
  d.	Then, SyncroSim call the second transformer, *Categorize Connectivity Output*. 
    i.	*Setting up Scenario* – the transformer takes an output from the first transformer along with the connectivity categories and their threshold values.
    ii.	*Categorizing connectivity output* – the transformer reclassifies the continuous output and returns it back to SyncroSim.
7.	When the run is complete, the *Status* will be updated to *Done*. You can inspect the **Run Log**, which returns the total run time for the scenario. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot39.png">

_**Step 4. Comparing results across scenarios**_
With two successful scenario runs, you will now compare their results. 
1.	Ensure that both scenarios are added to the results. This is noted by a red check mark beside the scenario symbol and a bolded scenario name. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot40.png">

If required, right-click on the scenario(s) and select **Add to Results** from the context menu.
2.	First, view the **Area** chart.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot41.png">

Note that the increase in resistance resulted in a small increase in the amount of *Impeded* and *Channelized* areas, and a decrease in the amount of *Diffuse* and *Intensified* areas.  
3.	Next, view the **Connectivity categories** map. 
Zoom in and pan through the map and try to identify where across the landscape those changes in connectivity occurred.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot42.png">

Visually identifying areas of change between scenarios may not be straightforward. For more quantitative tools to compare changes in connectivity, see the next tutorial <A href="#measuring-the-impact-of-connectivity-change-with-omniscapeimpact">Measuring the impact of connectivity change with **omniscapeImpact**</A>.

## **Measuring the impact of connectivity change with omniscapeImpact**

This tutorial guides you through using the **omniscapeImpact** add-on package to **omniscape SyncroSim**. It covers the following steps:
<A href="#step-1.-installing-the-omniscapeimpact-package">Step 1. Installing the omniscapeImpact package</A>
<A href="#step-2.-creating-and-configuring-an-omniscapeimpact-syncrosim-library">Step 2. Creating and configuring an omniscapeImpact SyncroSim Library</A>
<A href="#step-3.-visualizing-and-comparing-scenario-results">Step 3. Visualizing and comparing scenario results</A>

_**Requirements**_ #zzz: fix link
Before you begin, make sure that the **omniscape** SyncroSim package version 1.1.0 is installed. For more information, see <A href="#installing-the-omniscape-syncrosim-package">Installing the **omniscape** SyncroSim package</A>.

<br>

_**Step 1. Installing the omniscapeImpact package**_
1.	Open SyncroSim Desktop.
2.	Select **File > Packages**.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot43.png">

3.	The *Packages* window will open, listing all the SyncroSim packages installed in your computer. To install a new package from the Package Server, click **Install**.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot44.png">

4.	A new window will open listing the packages available for install from the Package Server. To install **omniscapeImpact**, mark the checkbox beside the package name and click **OK**. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot45.png">

5.	The **omniscapeImpact** package uses Conda to manage the package dependencies. Upon installing the package, you will be prompted to create or update the Conda environment for **omniscapeImpact**. Click **Yes**.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot46.png">

6.	Return to the *Packages* window, **omniscapeImpact** will now be listed along with the other installed packages, and the Conda checkbox will be marked.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot47.png">

_**Step 2. Creating and configuring an omniscapeImpact SyncroSim Library**_
1.	Open SyncroSim Desktop.
2.	To create a new library, select **File > New**.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot48.png">

  a.	From the list of packages, select **omniscape**.
  b.	Select the **Omniscape Impact** template library. If desired, you may edit the *File name*, and change the *Folder* by clicking on the *Browse* button. Click **OK**.
  
<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot49.png">

A new library will be created based on the selected template, and SyncroSim will automatically open and display it in the Library Explorer window.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot50.png">

1.	Note that the library contains two folders: *omniscape* and *omniscapeImpact*.
2.	Expand the **omniscape** folder and note that it contains three scenarios.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot51.png">

The first two scenarios were covered in the tutorial <A href="#reproducing-the-omniscape.jl-example-with-omniscape-syncrosim">Reproducing the Omniscape.jl example with **omniscape** SyncroSim</A>. 
The additional scenario, *Decreased resistance*, represents the case where resistance has been decreased by a similar magnitude as in the *Increased resistance* scenario.
3.	Next, expand the **omniscapeImpact** folder and note that it contains two scenarios:
  a.	*Impact of increased resistance* – compares the *Reference resistance* and *Increased resistance* scenarios.
  b.	*Impact of decreased resistance* – compares the *Reference resistance* and *Decreased resistance* scenarios.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot52.png">

4.	Double-click on *Impact of increased resistance* to open the scenario properties.
5.	Under the *General* tab, navigate to the **Pipeline** datasheet.
Note that it lists one pipeline stage, *Connectivity Impact Assessment*.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot53.png">

6.	Navigate to the **Add-on** tab. 
  a.	Under the *Impact Assessment* node, you will find the package’s only datasheet, called *Scenarios to Compare*. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot54.png">

It takes as input the ID of the two scenarios to be compared:
  i.	*Baseline Scenario ID* – represents the reference connectivity state from which changes will be measured. For this example, the ID is *1* corresponding to the *Reference resistance* scenario.
  ii.	*Alternative Scenario ID* – represents the changed connectivity state. For this example, the ID is *2* corresponding to the *Increased resistance* scenario.
7.	Close the scenario properties.

_**Step 3. Visualizing and comparing scenario results**_
The Omniscape Impact template library already contains the results for all its scenarios. In SyncroSim, the results for a scenario are organized into a Results folder, nested within its parent scenario. 
1.	In the Library Explorer window, click on the arrow beside the **Impact of increased resistance** scenario to expose the *Results* folder; repeat the same action to expose the results scenario. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot55.png">

2.	Double-click on the results scenario to open its properties.
3.	Navigate to the **Add-on** tab and expand the **Results** node. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot56.png">

The **omniscapeImpact** package generates spatial and tabular outputs. 
4.	Under the *Spatial* node are the following outputs:
  a.	*Overall* – represents per pixels change in normalized current flow or connectivity category. 
  b.	*Per Category* – represents per pixels loss, gain and no change for each connectivity category.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot57.png">

5.	Under the *Tabular* node are the following outputs:
  a.	*Differences Summary* – represents the change in area and percent cover between the baseline and alternative scenarios for each connectivity category.
  b.	*Transitions Summary* – represents the change in area and percent cover between the baseline and alternative scenarios for all possible transitions between connectivity categories.
  c.	*Jaccard Dissimilarity* – represents the dissimilarity between the baseline and alternative scenarios for each connectivity category. For each connectivity category, the Jaccard Dissimilarity is calculated as 1 minus the ratio between the number of shared pixels across scenarios and the total number of pixels across scenarios.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot58.png">

6.	Close the scenario properties and collapse the results and scenario folder.

You will now visualize the tabular outputs of **omniscapeImpact**.
7.	In the Library Explorer window, select the scenarios **Impact of increased resistance** and **Impact of decreased resistance**, right-click, and select **Add to Results** from the context menu. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot59.png">

8.	Navigate to the **Charts** tab and double-click to view the **Area difference** chart. 

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot60.png">

Note that the two scenarios had opposite effects on connectivity. 
The Increased resistance scenario led to an increase in area for *Impeded* and *Channelized* and a decrease in area for *Diffuse* and *Intensified*, relative to the Reference scenario. 
The Decreased resistance scenario led to a decrease in area for *Impeded* and *Channelized* and an increase in area for *Diffuse* and *Intensified*, relative to the Reference scenario. 
Note also that the magnitude of change in area was larger under the Decreased resistance scenario. 
9.	Close the *Area difference* chart and open the **Jaccard dissimilarity** chart.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot61.png">

Note that a similar pattern is reflected here, with *Impact of decreased resistance* showing greater dissimilarity to the baseline scenario compared to *Impact of increased resistance*.

Next, for a visual confirmation of the quantitative changes summarized by area and the Jaccard dissimilarity, you will inspect the spatial outputs of **omniscapeImpact**.
10.	Navigate to the **Maps** tab and double-click to open the **Normalized current difference** and **Cross-category difference** maps.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot62.png">

The *Normalized current difference* summarizes continuous change in current between the baseline and alternative scenarios.
In turn, the *Cross-category difference* map highlights pixels where the change in current represented a change in connectivity category. For example, a change from *Impeded* to *Diffuse* would represent a *1 category gain*, while a change from *Channelized* to *Diffuse* would represent a *2 category loss*.

11.	Close the *Normalized current difference* and open the **Per-category difference** map.

<img align="left" style="padding: 13px" width="180" src="assets/images/screenshot63.png">

The *Per-category difference* map represents per pixel losses and gains for each category. Together with the *Cross-category difference* map, it can be used to identify transitions between connectivity categories.
Both maps also highlight that a decrease in resistance had a stronger effect on connectivity than an increase.
