#
# Omniscape Example in R
#
# This script covers how to:
#   - reproduce the SyncroSim UI example in R
#   - run a sensitivity analysis with SyncroSim
#



# Workspace setup --------------------------------------------------------------

library(raster)
library(rsyncrosim)
library(ggplot2)
library(viridis)
library(scales)



# ------------------- Reproduce the SyncroSim UI example --------------------- #

# Open Library -----------------------------------------------------------------

myLibrary <- ssimLibrary(name = "omniscapeExample.ssim")
myProject <- project(ssimObject = myLibrary, project = "Definitions")


# Create and edit a new scenario -----------------------------------------------

# Load reference scenario
referenceScenario <- scenario(ssimObject = myProject, 
                              scenario = "Radius: 100 - Reference connectivity")

# Create copy of reference scenario
newScenario <- scenario(myProject, 
                        scenario = paste("Radius:", 25, "(built in R)"), 
                        sourceScenario = referenceScenario,
                        overwrite = T)
  
# Get desired datasheet
requiredInput <- datasheet(newScenario, name = "omniscape_Required")
  
# Enter new value
requiredInput$radius <- 25
  
# Save datasheet back to new scenario  
saveDatasheet(ssimObject = newScenario, 
              data = requiredInput, 
              name = "omniscape_Required")



# Run --------------------------------------------------------------------------

myResults <- run(newScenario)



# Get outputs ------------------------------------------------------------------

cumCurrent <- datasheetRaster(myResults,
                              datasheet = "omniscape_Results",
                              column = "cum_currmap")
flowPotential <- datasheetRaster(myResults,
                                 datasheet = "omniscape_Results",
                                 column = "flow_potential")
normCurrent <- datasheetRaster(myResults,
                               datasheet = "omniscape_Results",
                               column = "normalized_cum_currmap")



# Plot results -----------------------------------------------------------------

plot_omniscape <- function(output){

  if(all.equal(output, cumCurrent)){
    title_text <- "Cumulative Current Flow"
    reclassTable <- c(0, 0, 0,
                      0, 3, 3,
                      3, 10, 10,
                      10, 20, 20,
                      20, 50, 50,
                      50, 60, 60,
                      60, 80, 80,
                      80, 100, 100,
                      100, 400, 400,
                      400, Inf, 1000)
    outputDiscrete <- reclassify(output, reclassTable)
    breaks <- c(0, 3, 10, 20, 50, 60, 80, 100, 400, 1000)
  } 
  if(all.equal(output, flowPotential)){
    title_text <- "Flow Potential"
    reclassTable <- c(0, 0, 0,
                      0, 1, 1,
                      1, 2, 2,
                      2, 3, 3,
                      3, 5, 5,
                      5, 8, 8,
                      8, 10, 10,
                      10, 20, 20,
                      20, 40, 40,
                      40, Inf, 100)
    outputDiscrete <- reclassify(output, reclassTable)
    breaks <- c(0, 1, 2, 2, 5, 8, 10, 20, 40, 100)
  } 
  if(all.equal(output, normCurrent)){
    title_text <- "Normalized Current Flow"
    reclassTable <- c(0, 0, 0,
                      0, 0.1, 0.1,
                      0.1, 0.25, 0.25,
                      0.25, 0.5, 0.5,
                      0.5, 1.5, 1.5,
                      1.5, 2, 2,
                      2, 2.5, 2.5,
                      2.5, 3, 3,
                      3, 4, 4,
                      4, Inf, 100)
    outputDiscrete <- reclassify(output, reclassTable)
    breaks <- c(0, 0.1, 0.25, 0.5, 1.5, 2, 2.5, 3, 4, 100)
  } 
  
  # palette_colors <- c(inferno(10))
  # qntls <- as.vector(quantile(output, probs = seq(0, 1, 1/29)))
  
  # fill_values <- rescale(qntls, to = c(0, 1), from = c(min(qntls), max(qntls)))
  # 
  # output_pts <- rasterToPoints(outputDiscrete, spatial = TRUE, fun = NULL)
  # output_df  <- data.frame(output_pts)
  # colnames(output_df)[1] <- "variable"
  
  # ggplot(data = output_df, aes(x = x/100000, y = y/100000, fill = variable)) +
  #   geom_raster() +
  #   labs(title = "title_text", x = "Longitude", y = "Latitude") +
  #   scale_fill_gradientn(colours = palette_colors, 
  #                        values = fill_values,
  #                        name = "",
  #                        guide = guide_colorbar(barwidth = 0.8)) +
  #   scale_x_continuous(expand = c(0,0)) +
  #   scale_y_continuous(expand = c(0,0)) +
  #   theme_bw()
  
  palette_colors <- c("#000004", "#180F3E", "#450F76", "#721F81", "#9E2F7F",
                      "#CD3F71", "#DD5138", "#F47A18", "#FAC62D", "#F6FA96")
  
  output_df <- as.data.frame(outputDiscrete, xy = TRUE)
  colnames(output_df)[3] <- "variable"
  output_df$variable <- factor(output_df$variable)
  
  ggplot(data = output_df, aes(x = x/100000, y = y/100000, fill = variable)) +
    geom_raster() +
    labs(title = title_text, x = "Longitude", y = "Latitude") +
    scale_fill_manual(values = palette_colors,
                      breaks = breaks,
                      name = "") +
    scale_x_continuous(expand = c(0,0)) +
    scale_y_continuous(expand = c(0,0)) +
    theme_bw()
}

plot_omniscape(cumCurrent) 
plot_omniscape(flowPotential) 
plot_omniscape(normCurrent)

# Check scenario & results in the SyncroSim UI



# -------------------------- Sensitivity analysis ---------------------------- #

# Variable of interest
radii <- c(25, 50, 75, 100, 125, 150, 175, 200, 225)

# Output data frame
radii_runtime <- data.frame(radius = as.numeric(), runtime = as.numeric())

# Loop
for(radius in radii){
  
  # Create copy of reference scenario
  newScenario <- scenario(myProject, 
                          scenario = paste("Radius:", radius, "(built in R)"), 
                          sourceScenario = myScenario,
                          overwrite = T)
  
  # Get desired datasheet
  requiredInput <- datasheet(newScenario, name = "omniscape_Required")
  
  # Enter new value
  requiredInput$radius <- radius
  
  # Save datasheet back to new scenario  
  saveDatasheet(ssimObject = newScenario, 
                data = requiredInput, 
                name = "omniscape_Required")
  
  # Run
  startTime <- Sys.time()
  myResults <- run(newScenario)
  endTime <- Sys.time()
  runTime <- endTime - startTime
  
  # Save output
  temp_df <- data.frame(radius = radius, runtime = runTime)
  radii_runtime <- rbind(radii_runtime, temp_df)
}

# Write or read output
write.csv(radii_runtime, file = "radii_runtime_output.csv")
radii_runtime <- read.csv(file = "radii_runtime_output.csv", header = TRUE)[,-1]

# Plot radii vs. run time
ggplot(radii_runtime, aes(x = as.numeric(radius), y = as.numeric(runtime/60))) +
  xlab("Moving window radius") + ylab("Run time (min)") +
  geom_point() +
  geom_line() +
  theme_classic()


