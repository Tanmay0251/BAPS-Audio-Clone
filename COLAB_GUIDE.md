# 🚀 Google Colab Guide - BAPS Audio Generator

Complete step-by-step guide for generating personalized audio messages on Google Colab.

---

## Table of Contents

1. [Why Use Google Colab?](#why-use-google-colab)
2. [Before You Start](#before-you-start)
3. [Quick Start Guide](#quick-start-guide)
4. [Detailed Walkthrough](#detailed-walkthrough)
5. [Troubleshooting](#troubleshooting)
6. [Best Practices](#best-practices)

---

## Why Use Google Colab?

### Advantages:
- ✅ **Free GPU Access** - T4 GPU for faster processing (3-5x faster than CPU)
- ✅ **No Installation** - Everything runs in browser
- ✅ **Accessible Anywhere** - Just need internet and Google account
- ✅ **Perfect for Large Batches** - Ideal for 100-500 names

### Performance:
- **CPU**: 20-30 seconds per audio
- **GPU (T4)**: 5-10 seconds per audio
- **For 100 names**: 10-15 minutes (vs 40-50 minutes on CPU)

---

## Before You Start

### What You Need:

1. **Google Account** - For accessing Colab
2. **Reference Audio File** - MP4/WAV with voice to clone
   - Duration: 6-15 seconds (10-12 seconds ideal)
   - Quality: Clear speech, minimal background noise
   - Format: MP4, WAV, or MP3

3. **Names Sheet** - Excel (.xlsx) or CSV file
   - Must have a column with names
   - Can contain Hindi/English names
   - Example:
     ```
     Name
     राहुल कुमार
     John Smith
     प्रिया शर्मा
     ```

4. **Template Text** - Your message with `{name}` placeholder
   - Example: `"नमस्ते {name}, आपका स्वागत है।"`

---

## Quick Start Guide

### Step 1: Choose Your Notebook

#### **Basic Audio Generator** (`basic_audio_generator.ipynb`)
- **Use for**: <100 names, simple use case
- **Method**: Generates complete message for each name
- **Time**: ~20-30 seconds per name

#### **Optimized Audio Generator** (`optimized_audio_generator.ipynb`) ⭐ RECOMMENDED
- **Use for**: 100-500+ names, recurring batches
- **Method**: Splits audio → generates common parts once
- **Time**: ~5-10 seconds per name
- **Savings**: 60-70% faster!

### Step 2: Open in Colab

1. Go to GitHub repository
2. Click on the notebook file
3. Click "Open in Colab" button at the top

### Step 3: Enable GPU (IMPORTANT!)

```
1. Click "Runtime" in menu
2. Select "Change runtime type"
3. Under "Hardware accelerator": Select "T4 GPU"
4. Click "Save"
```

**⚠️ This step is crucial for faster processing!**

### Step 4: Run All Cells

```
1. Click "Runtime" → "Run all"
2. Wait for dependencies to install (~2-3 minutes)
3. Follow prompts to upload files
4. Wait for generation to complete
5. Download ZIP when done
```

---

## Detailed Walkthrough

### Using Basic Audio Generator

#### Cell 1: Setup & Installation
```python
# This cell installs all dependencies
# Takes 2-3 minutes on first run
# Shows GPU information
```
**Wait for**: "✅ Setup complete!"

#### Cell 2: Upload Files
```python
# Upload 1: Reference audio (MP4/WAV)
# Upload 2: Names sheet (Excel/CSV)
```
**Action**: Click "Choose Files" when prompted

#### Cell 3: Configuration
```python
# Set your template text
template_text = "नमस्ते {name}, आपका हार्दिक स्वागत है।"

# Set column name
name_column = "Name"  # Change if your column is named differently
```
**Action**: Edit the template and column name

#### Cell 4: Initialize Voice Cloner
```python
# Loads the AI model
# Tests voice with sample text
# Takes 1-2 minutes
```
**Wait for**: "✅ Voice cloner ready!"

#### Cell 5: Preview Names (Optional)
```python
# Shows first 5 names from your sheet
# Verifies column name is correct
```
**Check**: Names are loading correctly

#### Cell 6: Test with Samples (Optional but Recommended)
```python
# Generates audio for 3 sample names
# Lets you verify quality before full run
```
**Action**: Listen to the test audio and verify quality

#### Cell 7: Generate All
```python
# Generates audio for ALL names
# Shows progress bar
# Takes 10-50 minutes depending on count
```
**Wait**: Let it complete. Progress bar shows status.

#### Cell 8: Download
```python
# Creates ZIP file
# Downloads automatically
```
**Result**: ZIP file with all audio files

---

### Using Optimized Audio Generator

#### Setup (Cells 1-2)
Same as basic generator

#### Cell 3: Choose Mode
```python
generation_mode = "template"  # or "audio_files"
```

**Modes:**
- `"template"`: Splits text automatically
- `"audio_files"`: Uses pre-recorded prefix/suffix audio

#### Cell 4-6: Configuration & Setup
Same process as basic, but optimized

#### Cell 7: Generate All (Optimized)
```python
# Step 1: Generates prefix audio ONCE
# Step 2: Generates suffix audio ONCE
# Step 3: Generates name audio for each name
# Step 4: Merges all parts automatically
```

**Process:**
1. See prefix/suffix generation (once only)
2. Progress bar for name generation
3. Automatic merging
4. Much faster than basic!

#### Cell 8-9: Download & Cleanup
Same as basic

---

## Troubleshooting

### Issue: GPU Not Working
**Symptoms**: Very slow processing, no GPU mentioned in setup

**Solution:**
1. Runtime → Change runtime type → T4 GPU → Save
2. Runtime → Restart runtime
3. Run cells again

### Issue: "Column 'Name' not found"
**Symptoms**: Error when loading names

**Solution:**
1. Check your Excel/CSV file
2. Note the exact column name (case-sensitive)
3. Update `name_column = "YourColumnName"` in configuration cell

### Issue: "Reference audio is less than 6 seconds"
**Symptoms**: Warning about audio length

**Solution:**
1. Use longer reference audio (6-15 seconds recommended)
2. If you must use shorter audio, results may vary in quality

### Issue: Voice doesn't sound like original
**Symptoms**: Generated voice is different

**Solution:**
1. Use longer reference audio (10-15 seconds ideal)
2. Ensure reference audio has clear speech
3. Remove background noise from reference
4. Try re-generating with different reference audio

### Issue: Names pronounced incorrectly
**Symptoms**: English names sound wrong

**Solution:**
1. Write names in Hindi script (e.g., "जॉन" instead of "John")
2. Or accept the Hindi accent for English names
3. Test with a few names first

### Issue: Runtime disconnected
**Symptoms**: "Runtime disconnected" error

**Solution:**
1. Colab has time limits (free tier: ~4 hours)
2. If processing 500+ names, may need to split into batches
3. Reconnect and continue with remaining names

---

## Best Practices

### 1. Reference Audio Quality
- **Duration**: 10-12 seconds ideal
- **Content**: Clear speech, single speaker
- **Background**: Minimal to no background noise
- **Volume**: Consistent, not too loud or soft

### 2. Template Design
```python
# Good examples:
"नमस्ते {name}, आपका स्वागत है।"
"प्रिय {name}, BAPS परिवार की ओर से आपका हार्दिक स्वागत है।"

# Tips:
- Keep it natural and conversational
- Use proper punctuation
- Test with sample names first
```

### 3. Batch Size Recommendations

| Names | Notebook | Expected Time |
|-------|----------|---------------|
| <50 | Basic | 10-20 minutes |
| 50-100 | Basic or Optimized | 15-25 minutes |
| 100-300 | Optimized ⭐ | 15-30 minutes |
| 300-500 | Optimized ⭐ | 30-45 minutes |
| 500+ | Split into batches | Multiple runs |

### 4. Name Formatting

**In Your Sheet:**
```
Name
राहुल कुमार        ✅ Good - Hindi script
John Smith        ✅ Good - English (will have Hindi accent)
जॉन स्मिथ         ✅ Good - English in Hindi script
RAHUL KUMAR       ✅ Good - Will work fine
```

### 5. Testing Workflow

1. **First Time:**
   - Upload 5-10 sample names only
   - Generate and verify quality
   - Adjust template/settings if needed

2. **Full Run:**
   - Upload all names
   - Use optimized notebook for 100+
   - Let it run uninterrupted

3. **Quality Check:**
   - Listen to 2-3 random audios
   - Verify names are pronounced correctly
   - Check audio quality

---

## Cost & Limitations

### Google Colab Free Tier:
- **GPU Time**: Limited but generous for this use case
- **Session Duration**: ~4 hours max
- **Recommendation**: For 500+ names, split into batches of 200-300

### When to Upgrade:
- Regular use with 500+ names each time
- Need guaranteed GPU access
- Faster processing required

---

## Advanced: Pre-recorded Audio Mode

### When to Use:
- Generating 500+ names regularly
- Want professional voice over + AI names
- Same message, different name lists

### How It Works:

1. **Record Professionally:**
   - Prefix: "नमस्ते" → `prefix.mp3`
   - Suffix: "आपका स्वागत है" → `suffix.mp3`
   - Use professional recording/voice over

2. **In Optimized Notebook:**
   ```python
   generation_mode = "audio_files"
   ```

3. **Upload:**
   - Upload prefix audio
   - Upload suffix audio
   - Upload names list

4. **Generate:**
   - Only names are generated with AI
   - Merged with professional audio
   - **Cost/Time**: Only for name generation!

### Benefits:
- Zero cost for repeated text
- Professional quality for common parts
- AI only for names (faster + cheaper)
- Perfect for large-scale production

---

## FAQ

**Q: Can I use this for languages other than Hindi?**
A: Yes! Change `language="hi"` to other codes (en, es, fr, etc.)

**Q: How many names can I process at once?**
A: Recommended: 200-300 per batch on free Colab. Can do 500+ with Colab Pro.

**Q: Can I use my own voice?**
A: Yes! Just provide 10-15 seconds of clear recording as reference audio.

**Q: Is my data safe?**
A: Files are uploaded to your Colab session only. Deleted after session ends.

**Q: Can I download individual files instead of ZIP?**
A: Yes! Before running download cell, manually download from the `generated_audios` or `merged_audios` folder.

**Q: What if I need to stop and resume?**
A: Currently not supported. Plan for uninterrupted runs or split into smaller batches.

---

## Quick Comparison Table

| Feature | Basic Notebook | Optimized Notebook |
|---------|----------------|-------------------|
| Speed | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Complexity | Simple | Medium |
| Best For | <100 names | 100-500+ names |
| Pre-recorded Audio | ❌ | ✅ |
| Time Savings | - | 60-70% faster |
| Setup Steps | 8 cells | 9 cells |

---

## Support

For issues or questions:
1. Check this guide thoroughly
2. Review the Troubleshooting section
3. Verify GPU is enabled
4. Test with small batch first (5-10 names)
5. Check reference audio quality

---

**Ready to start?** Open `optimized_audio_generator.ipynb` in Colab and follow the guide! 🚀
