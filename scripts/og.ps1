# Genera las imágenes sociales (1200 x 630) a partir de scripts/og-manifest.json.
# Uso: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/og.ps1

Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent $PSScriptRoot
$manifestPath = Join-Path $PSScriptRoot 'og-manifest.json'
$outDir = Join-Path $root 'img\og'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$W = 1200
$H = 630

$colInk = [System.Drawing.ColorTranslator]::FromHtml('#1d1d1f')
$colInk2 = [System.Drawing.ColorTranslator]::FromHtml('#6e6e73')
$colAccent = [System.Drawing.ColorTranslator]::FromHtml('#0071e3')
$colBand = [System.Drawing.ColorTranslator]::FromHtml('#f5f5f7')

function Wrap-Lines {
  param($g, [string]$text, $font, [double]$maxW)
  $lines = New-Object System.Collections.Generic.List[string]
  $current = ''
  foreach ($word in ($text -split '\s+')) {
    $try = if ($current) { "$current $word" } else { $word }
    if ($g.MeasureString($try, $font).Width -gt $maxW -and $current) {
      $lines.Add($current)
      $current = $word
    } else {
      $current = $try
    }
  }
  if ($current) { $lines.Add($current) }
  return $lines
}

function Fit-Font {
  param($g, [string]$text, [double]$maxW, [int]$maxLines)
  foreach ($size in @(54, 48, 42, 36, 30)) {
    $font = New-Object System.Drawing.Font('Segoe UI', $size, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $lines = Wrap-Lines -g $g -text $text -font $font -maxW $maxW
    if ($lines.Count -le $maxLines) { return @{ Font = $font; Lines = $lines; Size = $size } }
    $font.Dispose()
  }
  $font = New-Object System.Drawing.Font('Segoe UI', 30, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
  $lines = Wrap-Lines -g $g -text $text -font $font -maxW $maxW
  return @{ Font = $font; Lines = $lines; Size = 30 }
}

function New-Card {
  param(
    [string]$OutFile,
    [string]$Kicker,
    [string]$Title,
    [string]$Subtitle,
    [string]$ImagePath
  )

  $bmp = New-Object System.Drawing.Bitmap $W, $H
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
  $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.Clear([System.Drawing.Color]::White)

  # Banda inferior
  $bBand = New-Object System.Drawing.SolidBrush $colBand
  $g.FillRectangle($bBand, 0, ($H - 84), $W, 84)

  # Imagen del producto (primero, para que el texto quede por encima)
  if (Test-Path $ImagePath) {
    $img = [System.Drawing.Image]::FromFile($ImagePath)
    $boxW = 460; $boxH = 330
    $scale = [Math]::Min($boxW / $img.Width, $boxH / $img.Height)
    $dw = [int]($img.Width * $scale); $dh = [int]($img.Height * $scale)
    $dx = 1150 - $dw
    $dy = 96 + [int](($boxH - $dh) / 2)
    $g.DrawImage($img, $dx, $dy, $dw, $dh)
    $img.Dispose()
  }

  # Kicker
  $fKick = New-Object System.Drawing.Font('Segoe UI', 24, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
  $bKick = New-Object System.Drawing.SolidBrush $colAccent
  $g.DrawString($Kicker, $fKick, $bKick, 80, 70)

  # Título
  $fit = Fit-Font -g $g -text $Title -maxW 570 -maxLines 3
  $bInk = New-Object System.Drawing.SolidBrush $colInk
  $y = 126
  foreach ($line in $fit.Lines) {
    $g.DrawString($line, $fit.Font, $bInk, 80, $y)
    $y += [int]($fit.Size * 1.16)
  }

  # Subtítulo
  $fSub = New-Object System.Drawing.Font('Segoe UI', 26, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
  $bInk2 = New-Object System.Drawing.SolidBrush $colInk2
  $subY = $y + 22
  foreach ($line in (Wrap-Lines -g $g -text $Subtitle -font $fSub -maxW 560)) {
    $g.DrawString($line, $fSub, $bInk2, 80, $subY)
    $subY += 34
  }

  # Pie
  $fFoot = New-Object System.Drawing.Font('Segoe UI', 21, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
  $fFootB = New-Object System.Drawing.Font('Segoe UI', 21, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
  $g.DrawString('ComparaPortátil', $fFootB, $bInk, 80, ($H - 58))
  $right = 'raulft721.github.io/portatiles'
  $rw = $g.MeasureString($right, $fFoot).Width
  $g.DrawString($right, $fFoot, $bInk2, (1120 - $rw), ($H - 58))

  $g.Dispose()

  $codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
  $ep = New-Object System.Drawing.Imaging.EncoderParameters 1
  $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, 88L)
  $bmp.Save($OutFile, $codec, $ep)
  $bmp.Dispose()

  $fKick.Dispose(); $fSub.Dispose(); $fFoot.Dispose(); $fFootB.Dispose(); $fit.Font.Dispose()
  $bKick.Dispose(); $bInk.Dispose(); $bInk2.Dispose(); $bBand.Dispose()
}

# Tarjeta genérica
New-Card -OutFile (Join-Path $outDir 'default.jpg') `
  -Kicker 'ComparaPortátil' `
  -Title 'Dos portátiles. Una decisión clara.' `
  -Subtitle '22 modelos · precio y notas por uso' `
  -ImagePath (Join-Path $root 'img\mba13-m5.jpg')

# Una tarjeta por modelo
$items = Get-Content $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($it in $items) {
  $out = Join-Path $outDir ("{0}.jpg" -f $it.slug)
  $img = Join-Path $root ($it.img -replace '/', '\')
  New-Card -OutFile $out -Kicker $it.brand -Title $it.name -Subtitle ("{0} · ficha técnica y notas por uso" -f $it.price) -ImagePath $img
}

$sum = Get-ChildItem $outDir -Filter *.jpg | Measure-Object -Property Length -Sum
"{0} imágenes, {1:N0} KB en total" -f $sum.Count, ($sum.Sum / 1KB)
