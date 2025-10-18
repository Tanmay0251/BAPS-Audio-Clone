"""
Voice Cloning Module for Google Colab
Uses F5-TTS for high-quality voice cloning and Hindi TTS with GPU support
"""

import os
import torch
import torchaudio
from pydub import AudioSegment
import warnings
warnings.filterwarnings('ignore')


class VoiceCloner:
    def __init__(self, reference_audio_path, use_gpu=True):
        """
        Initialize the voice cloner with reference audio using F5-TTS

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

        # Initialize F5-TTS model
        print("\n📥 Loading F5-TTS model... (first run downloads ~1GB)")
        from f5_tts.api import F5TTS
        self.tts = F5TTS(device=self.device)
        print("✓ F5-TTS model loaded successfully!")

        # Prepare reference audio
        self._prepare_reference_audio()

    def _prepare_reference_audio(self):
        """Convert reference audio to WAV format if needed (internal use only)"""
        # F5-TTS requires WAV, but store in temp folder to keep workspace clean
        # Store in hidden temp folder so user doesn't see it
        temp_dir = ".f5tts_internal"
        os.makedirs(temp_dir, exist_ok=True)

        # Convert to WAV if not already (F5-TTS needs WAV internally)
        if not self.reference_audio_path.endswith('.wav'):
            print(f"\n🔄 Processing reference audio...")
            # Create hidden temp directory
            wav_path = os.path.join(temp_dir, "reference.wav")

            # Load audio file
            audio = AudioSegment.from_file(self.reference_audio_path)

            # Export as WAV (mono, 24000 Hz - optimal for F5-TTS)
            audio = audio.set_channels(1).set_frame_rate(24000)
            audio.export(wav_path, format="wav")

            self.reference_audio_path = wav_path
            print(f"✓ Reference audio prepared (internal processing only)")
        else:
            # If already WAV, still copy to temp dir and resample if needed
            wav_path = os.path.join(temp_dir, "reference.wav")
            audio = AudioSegment.from_file(self.reference_audio_path)
            audio = audio.set_channels(1).set_frame_rate(24000)
            audio.export(wav_path, format="wav")
            self.reference_audio_path = wav_path

        # Check audio duration
        audio = AudioSegment.from_wav(self.reference_audio_path)
        duration = len(audio) / 1000.0  # Convert to seconds
        print(f"✓ Reference audio duration: {duration:.2f} seconds")

        if duration < 3:
            print("⚠ WARNING: Reference audio is less than 3 seconds.")
            print("  Recommendation: Use at least 5-10 seconds of clear speech for best results.")
        elif duration > 30:
            print("ℹ INFO: Reference audio is longer than 30 seconds.")
            print("  F5-TTS will use a portion of it. 5-10 seconds is optimal.")

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
            # F5-TTS generates WAV, so create temp WAV path in hidden folder
            if output_format == "mp3":
                temp_dir = ".f5tts_internal"
                os.makedirs(temp_dir, exist_ok=True)
                import uuid
                temp_wav = os.path.join(temp_dir, f"temp_{uuid.uuid4().hex[:8]}.wav")
                final_path = output_path if output_path.endswith('.mp3') else output_path.replace('.wav', '.mp3')
            else:
                temp_wav = output_path
                final_path = output_path

            # Generate speech with F5-TTS (produces smooth, high-quality audio)
            audio, sample_rate = self.tts.infer(
                ref_file=self.reference_audio_path,
                ref_text="",  # Auto-transcribe reference
                gen_text=text,
                remove_silence=True  # Clean output
            )

            # Save WAV
            torchaudio.save(temp_wav, audio, sample_rate)

            # Convert to MP3 if requested
            if output_format == "mp3":
                audio_segment = AudioSegment.from_wav(temp_wav)

                # Minimal processing - F5-TTS output is already very clean
                # Just add subtle fade and normalize
                audio_segment = audio_segment.fade_in(20).fade_out(20)
                audio_segment = audio_segment.normalize()

                # Export with highest quality
                audio_segment.export(
                    final_path,
                    format="mp3",
                    bitrate="320k",
                    parameters=["-q:a", "0"]
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
        print("🧪 Testing Voice Cloning with F5-TTS")
        print("="*50)

        output_path = "test_output.mp3"
        success = self.generate_audio(test_text, output_path, output_format="mp3")

        if success:
            print(f"\n✓ Test successful! Listen to {output_path} to verify voice quality.")
            return True
        else:
            print("\n❌ Test failed. Check error messages above.")
            return False
