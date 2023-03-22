---
layout: default
title: Getting started
permalink: /getting_started
---

# Getting started with **omniscape** SyncroSim

### Here we provide guided tutorials on **omniscape** SyncroSim, an open-source SyncroSim base package for running Omniscape.jl. 

The tutorials will introduce you to the basics of working with **omniscape** SyncroSim. The steps include:

* Installing SyncroSim and Julia
* Reproducing the Omniscape.jl example with **omniscape** SyncroSim
* Creating a reproducible workflow for **omniscape** SyncroSim in R

<br>

## **Installing SyncroSim and Julia**

Running **omniscape** SyncroSim requires that SyncroSim and Julia be installed on your computer. Download SyncroSim version 2.4.5 or higher [here](https://syncrosim.com/download/){:target="_blank"} and follow the installation prompts. Download Julia version 1.5.4 or higher [here](https://julialang.org/downloads/){:target="_blank"} and follow the installation prompts. Once these requirements are installed, you are ready to follow along with the tutorials.

<br>

## **Reproducing the Omniscape.jl example with omniscape SyncroSim**

This video tutorial will provide an overview of working with **omniscape** SyncroSim in the Windows user interface and demonstrate how to reproduce the [Omniscape.jl example](https://docs.circuitscape.org/Omniscape.jl/stable/examples/){:target="_blank"}. 

The steps include:

* Installing **omniscape** SyncroSim
* Creating and configuring a new **omniscape** SyncroSim Library
* Creating and editing scenarios
* Running the model
* Visualizing the results

<iframe width="560" height="315" src="https://www.youtube.com/embed/jnTltF54xFU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

> **Note:** Before running a scenario, you need to specify the path to the Julia executable file. To do so, open the Library Properties, and under the Julia Configuration datasheet, click on the import button to navigate to the Julia executable file. If in the default location, you will find it at C:\Users\User_Name\AppData\Local\Programs\Julia-1.8.2\bin\julia.exe. The AppData folder is sometimes hidden. To see it, in File explorer, select View > Show > Hidden items.

<br>

## **Creating a reproducible workflow for omniscape SyncroSim in R**

This video tutorial will cover how to use the [rsyncrosim](https://syncrosim.github.io/rsyncrosim/){:target="_blank"} R package to interact with **omniscape** SyncroSim in R.

If you'd like to follow along with the tutorial, download R and the R Studio IDE [here](https://posit.co/download/rstudio-desktop/){:target="_blank"} and follow the installation prompts. 

> **Note:** If you are running **omniscape** using Conda, you must install [rsyncrosim](https://syncrosim.github.io/rsyncrosim/){:target="_blank"} [version 1.4.4](https://github.com/syncrosim/rsyncrosim/releases){:target="_blank"} or higher from GitHub.

The topics covered in the video tutorial include:
* Reproducing the Omniscape.jl example in R using rsyncrosim
* Performing a sensitivity analysis on an **omniscape** SyncroSim parameter

<iframe width="560" height="315" src="https://www.youtube.com/embed/x9sMm_BhwE0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<br>