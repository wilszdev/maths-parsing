workspace "MathsParsing"
    architecture "x64"
    configurations { "Debug", "Release", "Dist" }
    startproject "maths_parser"

outputdir = "%{cfg.buildcfg}-%{cfg.system}-%{cfg.architecture}"

include "maths_parser"
