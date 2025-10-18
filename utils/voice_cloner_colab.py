"""
Voice Cloning Module for Google Colab
Uses Coqui XTTS v2 for voice cloning and Hindi TTS with GPU support
"""

import os
import torch
from TTS.api import TTS
from pydub import AudioSegment
import warnings
warnings.filterwarnings('ignore')


class VoiceCloner:
    def __init__(self, reference_audio_path, use_gpu=True):
        """
        Initialize the voice cloner with reference audio

        Args:
            reference_audio_path: Path to the reference audio file (MP4, WAV, etc.)
            use_gpu: Use GPU if available (recommended for Colab)
        """
        self.reference_audio_path = reference_audio_path

        # Check GPU availability
        if use_gpu and torch.cuda.is_available():
            self.device = "cuda"
            print(f"✓ GPU detected: {torch.cuda.get_device_name(0)}")
            print(f"  VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        else:
            self.device = "cpu"
            print(f"⚠ Using CPU (will be slower)")

        # Initialize XTTS model
        print("\n📥 Loading XTTS model... (first run downloads ~2GB)")
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
        print("✓ Model loaded successfully!")

        # Prepare reference audio
        self._prepare_reference_audio()

    def _prepare_reference_audio(self):
        """Convert reference audio to WAV format if needed"""
        # Convert to WAV if not already (XTTS requires WAV internally)
        # Store in hidden temp folder so user doesn't see it
        if not self.reference_audio_path.endswith('.wav'):
            print(f"\n🔄 Processing reference audio...")
            # Create hidden temp directory
            temp_dir = ".xtts_internal"
            os.makedirs(temp_dir, exist_ok=True)
            wav_path = os.path.join(temp_dir, "reference.wav")

            # Load audio file
            audio = AudioSegment.from_file(self.reference_audio_path)

            # Export as WAV (mono, 22050 Hz - required by XTTS internally)
            audio = audio.set_channels(1).set_frame_rate(22050)
            audio.export(wav_path, format="wav")

            self.reference_audio_path = wav_path
            print(f"✓ Reference audio prepared (internal processing only)")

        # Check audio duration
        audio = AudioSegment.from_wav(self.reference_audio_path)
        duration = len(audio) / 1000.0  # Convert to seconds
        print(f"✓ Reference audio duration: {duration:.2f} seconds")

        if duration < 6:
            print("⚠ WARNING: Reference audio is less than 6 seconds.")
            print("  Recommendation: Use at least 6-15 seconds of clear speech for best results.")
        elif duration > 30:
            print("ℹ INFO: Reference audio is longer than 30 seconds.")
            print("  XTTS will use a portion of it. 10-15 seconds is optimal.")

    def generate_audio(self, text, output_path, language="hi", show_progress=True, output_format="mp3"):
        """
        Generate audio from text using the cloned voice

        Args:
            text: Text to synthesize (Hindi or mixed Hindi-English)
            output_path: Path to save the generated audio
            language: Language code (default: "hi" for Hindi)
            show_progress: Show progress message
            output_format: Output format - "mp3" or "wav" (default: "mp3")

        Returns:
            bool: True if successful, False otherwise
        """
        if show_progress:
            preview = text[:50] + "..." if len(text) > 50 else text
            print(f"🎤 Generating: {preview}")

        try:
            # TTS generates WAV, so create temp WAV path in hidden folder
            if output_format == "mp3":
                temp_dir = ".xtts_internal"
                os.makedirs(temp_dir, exist_ok=True)
                import uuid
                temp_wav = os.path.join(temp_dir, f"temp_{uuid.uuid4().hex[:8]}.wav")
                final_path = output_path if output_path.endswith('.mp3') else output_path.replace('.wav', '.mp3')
            else:
                temp_wav = output_path
                final_path = output_path

            # Generate speech with optimized XTTS parameters to reduce artifacts
            self.tts.tts_to_file(
                text=text,
                file_path=temp_wav,
                speaker_wav=self.reference_audio_path,
                language=language,
                temperature=0.65,  # Lower = more stable/consistent voice (default 0.85)
                length_penalty=1.2,  # Slightly slower/more deliberate speech
                repetition_penalty=5.0,  # Prevent stuttering/repetition
                top_k=50,  # Reduce randomness for smoother output
                top_p=0.85  # Focus on most probable tokens
            )

            # Convert to MP3 if requested
            if output_format == "mp3":
                audio = AudioSegment.from_wav(temp_wav)

                # Minimal processing - only essential smoothing
                # 1. Very subtle fade in/out (20ms)
                audio = audio.fade_in(20).fade_out(20)

                # 2. Gentle normalization
                audio = audio.normalize()

                # Export with highest quality settings (no filters/compression)
                audio.export(
                    final_path,
                    format="mp3",
                    bitrate="320k",  # Maximum MP3 bitrate
                    parameters=["-q:a", "0", "-ar", "22050"]  # Highest quality, match XTTS sample rate
                )

                # Remove temp WAV file
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)

            if show_progress:
                print(f"✓ Saved: {final_path}")

            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def test_voice(self, test_text="नमस्ते, यह एक परीक्षण है।"):
        """Test the voice cloning with a sample text"""
        print("\n" + "="*50)
        print("🧪 Testing Voice Cloning")
        print("="*50)

        output_path = "test_output.mp3"
        success = self.generate_audio(test_text, output_path, output_format="mp3")

        if success:
            print(f"\n✓ Test successful! Listen to {output_path} to verify voice quality.")
            return True
        else:
            print("\n❌ Test failed. Check error messages above.")
            return False
