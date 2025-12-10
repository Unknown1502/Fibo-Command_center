# HDR/16-bit Export Testing Guide

## Overview
This guide demonstrates FIBO Command Center's professional HDR and 16-bit export capabilities with 4 tone mapping algorithms and multiple color space support.

## Test Scenarios

### Scenario 1: E-commerce Product Photography
**Objective:** Export high-quality product images with accurate color reproduction

**Steps:**
1. Generate product image with parameters:
   ```json
   {
     "camera_angle": "eye_level",
     "field_of_view": "normal",
     "lighting": "studio",
     "color_palette": "neutral",
     "composition": "centered",
     "style": "realistic"
   }
   ```

2. Export configurations to test:
   - **Standard Web:** Reinhard + sRGB + 8-bit PNG
   - **Print Ready:** ACES + Adobe RGB + 16-bit TIFF
   - **Archive:** Linear + Rec.2020 + 32-bit EXR

3. Compare results for:
   - Color accuracy
   - Detail preservation
   - File size vs quality
   - Print suitability

**Expected Results:**
- 8-bit PNG: ~2-5 MB, perfect for web
- 16-bit TIFF: ~50-100 MB, print ready
- 32-bit EXR: ~100-200 MB, maximum quality

---

### Scenario 2: Cinematic Lighting
**Objective:** Test tone mapping algorithms on high dynamic range scenes

**Steps:**
1. Generate dramatic scene:
   ```json
   {
     "lighting": "hard",
     "color_palette": "vibrant",
     "style": "cinematic"
   }
   ```

2. Apply all 4 tone mapping algorithms:
   - **Reinhard:** Natural, balanced highlights and shadows
   - **Filmic:** Cinematic curve, film-like contrast
   - **ACES:** Industry standard, accurate color science
   - **Uncharted2:** Game-like, high contrast, punchy

3. Compare side-by-side:
   - Highlight preservation
   - Shadow detail
   - Color grading
   - Overall mood

**Visual Comparison Grid:**
```
+------------------+------------------+
|    Reinhard      |     Filmic       |
| (Natural)        | (Cinematic)      |
+------------------+------------------+
|      ACES        |   Uncharted2     |
| (Standard)       | (Game-like)      |
+------------------+------------------+
```

---

### Scenario 3: Wide Color Gamut Test
**Objective:** Compare color space capabilities

**Steps:**
1. Generate vibrant scene:
   ```json
   {
     "color_palette": "vibrant",
     "lighting": "golden_hour"
   }
   ```

2. Export in all color spaces:
   - **sRGB:** Standard web (smallest gamut)
   - **DCI-P3:** Cinema display (wider than sRGB)
   - **Rec.2020:** Ultra HD TV (very wide)
   - **Adobe RGB:** Professional print (photography standard)

3. Compare on wide-gamut display:
   - Color richness
   - Saturation depth
   - Gamut clipping
   - Display compatibility

**Color Gamut Coverage:**
- sRGB: 100% baseline
- DCI-P3: ~125% of sRGB
- Adobe RGB: ~135% of sRGB
- Rec.2020: ~170% of sRGB

---

### Scenario 4: Bit Depth Comparison
**Objective:** Demonstrate benefits of 16-bit vs 8-bit

**Steps:**
1. Generate gradient scene (tests banding)

2. Export both versions:
   - 8-bit: 256 values per channel
   - 16-bit: 65,536 values per channel

3. Apply heavy color grading to reveal differences:
   - Increase exposure +2 stops
   - Adjust shadows/highlights
   - Look for banding in gradients

**Expected Observations:**
- 8-bit: Visible banding in smooth gradients
- 16-bit: Smooth, no banding artifacts
- File size: 16-bit is 2x larger

---

## Performance Benchmarks

### Processing Times (1920x1080 image)
- **Reinhard:** ~3 seconds
- **Filmic:** ~3.5 seconds
- **ACES:** ~4 seconds
- **Uncharted2:** ~4 seconds

### File Sizes
| Format | 8-bit | 16-bit | 32-bit |
|--------|-------|--------|--------|
| PNG    | 2 MB  | 12 MB  | N/A    |
| JPEG   | 1 MB  | N/A    | N/A    |
| TIFF   | 6 MB  | 50 MB  | 100 MB |
| EXR    | N/A   | N/A    | 150 MB |
| WebP   | 1 MB  | 8 MB   | N/A    |

---

## Quality Checklist

### For Each Export, Verify:
- ✅ No visible banding in gradients
- ✅ Preserved highlight details (no blown-out whites)
- ✅ Retained shadow information (no crushed blacks)
- ✅ Accurate color reproduction
- ✅ Appropriate file format for use case
- ✅ Correct bit depth and color space metadata
- ✅ No compression artifacts

---

## Use Case Recommendations

### Web Publishing
- **Format:** PNG or WebP
- **Bit Depth:** 8-bit
- **Color Space:** sRGB
- **Tone Mapping:** Reinhard or Filmic
- **Rationale:** Best compatibility, small file size

### Professional Print
- **Format:** TIFF
- **Bit Depth:** 16-bit
- **Color Space:** Adobe RGB
- **Tone Mapping:** ACES
- **Rationale:** Maximum quality, accurate colors

### Cinema/Video
- **Format:** EXR or TIFF
- **Bit Depth:** 16-bit or 32-bit
- **Color Space:** DCI-P3 or Rec.2020
- **Tone Mapping:** ACES or Filmic
- **Rationale:** Industry standard, HDR support

### Archival Storage
- **Format:** EXR
- **Bit Depth:** 32-bit float
- **Color Space:** Rec.2020
- **Tone Mapping:** None (Linear)
- **Rationale:** Maximum flexibility for future editing

---

## Testing Script

Save images in this structure:
```
hdr_tests/
├── scenario_1_ecommerce/
│   ├── original.png
│   ├── reinhard_srgb_8bit.png
│   ├── aces_adobergb_16bit.tiff
│   └── linear_rec2020_32bit.exr
├── scenario_2_cinematic/
│   ├── reinhard.png
│   ├── filmic.png
│   ├── aces.png
│   └── uncharted2.png
├── scenario_3_color_gamut/
│   ├── srgb.png
│   ├── dci_p3.png
│   ├── rec2020.png
│   └── adobe_rgb.tiff
└── scenario_4_bit_depth/
    ├── 8bit_gradient.png
    └── 16bit_gradient.tiff
```

---

## Known Limitations

1. **Browser Support:** Some color spaces require specific display hardware
2. **File Size:** 16/32-bit files are significantly larger
3. **Processing Time:** Higher bit depths take longer to process
4. **Compatibility:** EXR requires special viewers/software

---

## Conclusion

FIBO Command Center's HDR/16-bit export system provides professional-grade flexibility for any production pipeline, from web publishing to cinema-quality archival storage.

**Key Advantages:**
- 4 tone mapping algorithms for different aesthetics
- 4 color spaces for various display targets
- 3 bit depths (8/16/32) for quality vs file size balance
- 5 format options for compatibility
- Batch processing support for production workflows
