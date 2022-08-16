project "maths_parser"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    targetdir "bin/%{cfg.buildcfg}"
    staticruntime "off"
    warnings "Extra"

    files { "src/**.h", "src/**.cpp" }

    targetdir ("../bin/" .. outputdir .. "/%{prj.name}")
    objdir ("../bin-int/" .. outputdir .. "/%{prj.name}")

    filter "system:windows"
        systemversion "latest"
        defines { "PLATFORM_WINDOWS" }

    filter "configurations:Debug"
        defines { "CFG_DEBUG" }
        runtime "Debug"
        symbols "On"

    filter "configurations:Release"
        defines { "CFG_RELEASE" }
        runtime "Release"
        symbols "On"
        optimize "On"

    filter "configurations:Dist"
        kind "WindowedApp"
        defines { "CFG_DIST" }
        runtime "Release"
        symbols "Off"
        optimize "On"
