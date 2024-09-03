@echo off
setlocal enabledelayedexpansion

:: 初始化變數
set "root_dir="
set "exclude_dir="
set "quality=75"
set "config_file=webp-config.ini"
set "output_folder=webp-img"

:: 顯示用法說明
echo Usage: %~nx0
echo Configuration file: %config_file%
echo Converts images to WebP format while preserving folder structure.
echo The output files will be saved in a new folder named '%output_folder%' with the same structure as the original.
echo.
echo Example webp-config.ini:
echo root_dir=D:\path\to\assets\img
echo exclude_dir=D:\path\to\assets\img\
echo quality=75
echo.
echo For more details, visit: https://developers.google.com/speed/webp/docs/cwebp

:: 讀取配置檔案
if exist "%config_file%" (
    for /f "tokens=1,2 delims==" %%A in (%config_file%) do (
        if "%%A"=="root_dir" set "root_dir=%%B"
        if "%%A"=="exclude_dir" set "exclude_dir=%%B"
        if "%%A"=="quality" set "quality=%%B"
    )
) else (
    echo Error: Config file "%config_file%" not found.
    exit /b
)

:: 檢查是否設置了路徑
if "%root_dir%"=="" (
    echo Error: You must specify a path in the config file.
    exit /b
)

:: 檢查路徑是否存在
if not exist "%root_dir%" (
    echo Error: Directory does not exist: "%root_dir%"
    exit /b
)

:: 設置輸出根目錄
for %%I in ("%root_dir%") do set "parent_dir=%%~dpI"
set "output_root_dir=%parent_dir%%output_folder%"

:: 確保輸出根目錄存在
if not exist "%output_root_dir%" (
    mkdir "%output_root_dir%"
)

:: 顯示輸出結果路徑
echo Output files will be saved in the new folder structure under: %output_root_dir%
echo.

:: 確認是否執行
set /p user_input="Do you want to proceed with the conversion and copying? (y/n): "
if /i not "%user_input%"=="y" (
    echo Aborting the operation.
    exit /b
)

:: 複製所有資料夾結構（包括空資料夾）
echo Copying folder structure...
robocopy "%root_dir%" "%output_root_dir%" /E /XF *

:: 複製排除目錄的內容
if not "%exclude_dir%"=="" (
    echo Copying excluded directory contents...
    set "exclude_output_dir=%output_root_dir%!exclude_dir:%root_dir%=!"
    robocopy "%exclude_dir%" "!exclude_output_dir!" /E
)

:: 遍歷指定目錄下所有的文件
for /r "%root_dir%" %%i in (*.jpg *.png) do (
    :: 檢查是否在排除的資料夾中
    set "current_path=%%~dpi"
    if /i not "!current_path:~0,-1!"=="%exclude_dir%" (
        :: 如果不在排除的資料夾中，轉換為WebP
        set "file_path=%%i"
        set "relative_path=!file_path:%root_dir%=!"
        set "output_path=%output_root_dir%!relative_path!"
        set "output_dir=%%~dpi"
        set "output_dir=!output_dir:%root_dir%=%output_root_dir%!"
        
        echo Converting "%%i" to WebP with quality %quality%...
        cwebp -q %quality% "%%i" -o "!output_path:~0,-4!.webp"
    )
)

echo All operations completed!
pause