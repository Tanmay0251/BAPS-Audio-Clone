# BAPS Voice Cloning & Audio Generator

Voice cloning system for Pu. Prasannamuni Swami's voice to generate personalized Hindi audio messages.

## Features

- ✓ Clone voice from reference audio (original.mp4)
- ✓ Generate Hindi audio with cloned voice
- ✓ Handle English names with Hindi pronunciation
- ✓ Batch process names from Excel/CSV files
- ✓ Automatic audio file generation and organization
- ✓ **Google Colab support** with GPU acceleration
- ✓ **Optimized generation** - 60-70% faster for large batches (100-500 names)

## Quick Start (Recommended: Google Colab)

### 🚀 For 100-500 Names - Use Google Colab with GPU

**Why Colab?**
- Free GPU access (T4 GPU)
- No local setup required
- 3-5x faster than CPU
- Perfect for large batches

### Choose Your Notebook:

#### 1. **Basic Audio Generator** (`basic_audio_generator.ipynb`)
- Simple and straightforward
- Upload sheet + enter template → Get all audios
- Good for: <100 names or simple use cases
- Time: ~20-30 seconds per name

#### 2. **Optimized Audio Generator** (`optimized_audio_generator.ipynb`) ⭐ RECOMMENDED
- Smart audio splitting and merging
- 60-70% faster for large batches
- Good for: 100-500+ names
- Time: ~5-10 seconds per name
- **How it works:**
  - Splits template: "नमस्ते {name}, स्वागत है" → prefix + name + suffix
  - Generates common parts once
  - Only generates names individually
  - Merges automatically
  - **Future ready**: Can use pre-recorded audio files

### 🎯 How to Use Colab Notebooks:

1. **Open in Colab:**
   - Click on notebook file in GitHub
   - Click "Open in Colab" button

2. **Enable GPU:**
   - Runtime → Change runtime type
   - Hardware accelerator: T4 GPU
   - Save

3. **Run all cells:**
   - Runtime → Run all
   - Follow instructions in notebook
   - Upload your files when prompted

4. **Download results:**
   - ZIP file will download automatically
   - Contains all generated audio files

---

## Local Setup Instructions (Alternative)

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

**Note:** First time running will download the XTTS model (~2GB). This is one-time only.

### 2. Prepare Your Reference Audio

- Place your reference audio as `original.mp4` in this directory
- **Optimal quality:** 6-15 seconds of clear, clean speech
- **Minimum:** 6 seconds
- Voice should be clear without background noise

### 3. Test Voice Cloning

```bash
python voice_cloner.py
```

This will:
- Convert your MP4 to WAV format
- Load the XTTS model
- Generate test audio files
- Verify voice quality

### 4. Prepare Your Names Sheet

Create an Excel (.xlsx) or CSV file with names:

**Example: names.xlsx**
```
Name
राहुल कुमार
John Smith
प्रिया शर्मा
David Johnson
अमित पटेल
```

### 5. Generate Batch Audio

Edit `batch_audio_generator.py` to set your template:

```python
# Your Hindi template with {name} placeholder
template = "नमस्ते {name}, आपका हार्दिक स्वागत है।"

# Initialize generator
generator = BatchAudioGenerator(
    reference_audio_path="original.mp4",
    template_text=template
)

# Generate from your sheet
generator.generate_from_sheet("names.xlsx", name_column="Name")
```

Run the generator:

```bash
python batch_audio_generator.py
```

## Usage Examples

### Example 1: Simple Template

```python
template = "नमस्ते {name}, आपका स्वागत है।"
# Output: "नमस्ते John, आपका स्वागत है।"
```

### Example 2: Complex Template

```python
template = """प्रिय {name},
BAPS परिवार की ओर से आपका हार्दिक स्वागत है।
आशा है आप सभी स्वस्थ और प्रसन्न हैं।"""
```

### Example 3: Custom Column Name

```python
# If your sheet has column named "Full_Name"
generator.generate_from_sheet("data.xlsx", name_column="Full_Name")
```

### Example 4: Generate Single Audio

```python
generator.generate_single("राहुल")
# Creates: generated_audios/राहुल.wav
```

## Output

All generated audio files are saved in the `generated_audios/` folder with format:
- `Name_YYYYMMDD_HHMMSS.wav` (for batch processing)
- `Name.wav` (for single generation)

## Tips for Best Results

1. **Reference Audio Quality:**
   - Use 10-15 seconds of clear speech
   - Minimize background noise
   - Consistent volume and tone

2. **Name Pronunciation:**
   - English names will be pronounced with Hindi accent automatically
   - You can write names in Hindi script for better control
   - Example: "John" vs "जॉन"

3. **Template Design:**
   - Keep sentences natural and conversational
   - Test with sample names first
   - Use proper Hindi grammar and punctuation

4. **Performance:**
   - First run downloads model (~2GB)
   - GPU recommended for faster generation
   - CPU works but slower (~30-60 sec per audio)

## Troubleshooting

### Issue: "Reference audio is less than 6 seconds"
**Solution:** Use a longer audio clip (6-15 seconds is optimal)

### Issue: Voice doesn't sound like original
**Solution:**
- Check reference audio quality
- Use a longer reference clip (10-15 seconds)
- Ensure reference audio is clear without background noise

### Issue: English names not pronounced correctly
**Solution:**
- Try writing the name in Hindi script (e.g., "जॉन" instead of "John")
- Or use transliteration in the template

### Issue: Slow generation
**Solution:**
- Use GPU if available (CUDA)
- Each audio takes 30-60 seconds on CPU
- Be patient for batch processing

## Project Structure

```
BAPS_Gen_Audio/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── original.mp4                        # Your reference audio
│
├── 📓 Google Colab Notebooks
│   ├── basic_audio_generator.ipynb           # Simple batch generation
│   └── optimized_audio_generator.ipynb       # Optimized for 100-500 names ⭐
│
├── 🐍 Local Python Scripts (optional)
│   ├── voice_cloner.py                 # Original voice cloning script
│   └── batch_audio_generator.py        # Original batch processing
│
├── 🛠️ Utils (for Colab)
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── voice_cloner_colab.py       # Voice cloner with GPU support
│   │   ├── batch_generator.py          # Batch processing module
│   │   └── audio_merger.py             # Audio splitting & merging ⚡
│
└── 📁 Output Folders (auto-created)
    ├── generated_audios/               # Basic generation output
    ├── merged_audios/                  # Optimized generation output
    └── test_output.wav                 # Test files
```

## Performance Comparison

### Basic Method:
- Generates full message for each name
- Time: ~20-30 seconds per name on GPU
- For 100 names: ~40-50 minutes
- Use: `basic_audio_generator.ipynb`

### Optimized Method (Audio Splitting): ⚡
- Generates common parts once
- Only generates name per person
- Time: ~5-10 seconds per name on GPU
- For 100 names: ~10-15 minutes
- **60-70% faster!**
- Use: `optimized_audio_generator.ipynb`

### When to Use Which:
- **Basic**: <50 names, simple templates, one-time use
- **Optimized**: 100-500+ names, recurring use, professional setup

## Advanced Usage

### Future Enhancement: Pre-recorded Audio Files

The optimized notebook supports using pre-recorded audio files:

1. **Record professionally:**
   - Prefix: "नमस्ते" (or any greeting)
   - Suffix: "आपका स्वागत है। आशा है..." (or any message)

2. **Use in optimized notebook:**
   - Set mode to `"audio_files"`
   - Upload prefix and suffix audio files
   - Upload names list
   - **Cost: Only pay for name generation!**

3. **Benefits:**
   - Zero cost for repeated text
   - Consistent quality
   - Professional voice over + AI names
   - Perfect for 500+ names

### Use Different Languages

```python
# For mixed Hindi-English
cloner.generate_audio(text, output_path, language="hi")

# The model supports: en, es, fr, de, it, pt, pl, tr, ru, nl, cs, ar, zh-cn, ja, hi
```

### Process Multiple Sheets

```python
sheets = ["devotees_batch1.xlsx", "devotees_batch2.xlsx"]
for sheet in sheets:
    generator.generate_from_sheet(sheet)
```

### Custom Filename Format

Edit the `sanitize_filename` method in `batch_audio_generator.py` to customize output filenames.

## Requirements

### For Google Colab (Recommended):
- Google account
- Modern web browser
- Internet connection
- No local installation needed!

### For Local Setup:
- Python 3.8+
- 4GB RAM minimum (8GB+ recommended)
- GPU optional (CUDA) for faster processing
- ~3GB disk space for model

## Workflow Recommendation

### For 100-500 Names (Production):

1. **First Time Setup:**
   - Use `optimized_audio_generator.ipynb` on Colab
   - Upload reference audio
   - Test with 2-3 names
   - Verify quality

2. **Generate All:**
   - Upload full names sheet
   - Let it run (10-20 minutes for 100-500 names)
   - Download ZIP

3. **For Future Batches:**
   - Option A: Reuse the notebook (from template)
   - Option B: Record prefix/suffix professionally, use audio files mode

### For Testing/Small Batches (<50 names):
- Use `basic_audio_generator.ipynb`
- Simpler, fewer steps

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify your reference audio quality (6-15 seconds recommended)
3. Test with simple examples first
4. Use GPU runtime in Colab for faster processing
5. For 100+ names, always use the optimized notebook

---

**Note:** This system uses Coqui XTTS v2 for voice cloning. The voice is cloned once from your reference audio and can be reused indefinitely to generate any text.
