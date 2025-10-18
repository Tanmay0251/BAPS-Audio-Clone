"""
Audio Merger Module for Optimized Audio Generation
Splits audio generation and merges parts to save computation cost
"""

import os
from pydub import AudioSegment
from tqdm.auto import tqdm
import re


class AudioMerger:
    """
    Optimized audio generation by splitting into:
    - Prefix audio (generated once)
    - Name audio (generated per name)
    - Suffix audio (generated once)
    Then merges them for each name
    """

    def __init__(self, voice_cloner, output_dir="merged_audios"):
        """
        Initialize audio merger

        Args:
            voice_cloner: VoiceCloner instance
            output_dir: Directory to save merged audio files
        """
        self.voice_cloner = voice_cloner
        self.output_dir = output_dir
        self.temp_dir = os.path.join(output_dir, "_temp")

        # Create directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

        print(f"📁 Output directory: {self.output_dir}")
        print(f"📁 Temp directory: {self.temp_dir}")

    def sanitize_filename(self, name):
        """Convert name to safe filename"""
        safe_name = re.sub(r'[^\w\s-]', '', name)
        safe_name = re.sub(r'\s+', '_', safe_name)
        return safe_name[:100]

    def split_template(self, template):
        """
        Split template into prefix, placeholder, and suffix

        Args:
            template: Template string with {name} placeholder
                     Example: "नमस्ते {name}, आपका स्वागत है।"

        Returns:
            tuple: (prefix, suffix) or None if {name} not found
        """
        if "{name}" not in template:
            print("❌ Template must contain {name} placeholder")
            return None

        parts = template.split("{name}", 1)
        prefix = parts[0].strip()
        suffix = parts[1].strip() if len(parts) > 1 else ""

        return prefix, suffix

    def generate_common_audio(self, template, language="hi"):
        """
        Generate prefix and suffix audio files (one time only)

        Args:
            template: Template string with {name} placeholder
            language: Language code (default: "hi" for Hindi)

        Returns:
            tuple: (prefix_path, suffix_path) or None if failed
        """
        print(f"\n{'='*60}")
        print(f"🎬 Generating Common Audio Parts")
        print(f"{'='*60}")

        split_result = self.split_template(template)
        if split_result is None:
            return None

        prefix, suffix = split_result

        prefix_path = None
        suffix_path = None

        # Generate prefix audio
        if prefix:
            print(f"\n📝 Prefix: {prefix}")
            prefix_path = os.path.join(self.temp_dir, "prefix.wav")
            success = self.voice_cloner.generate_audio(
                text=prefix,
                output_path=prefix_path,
                language=language,
                show_progress=True
            )
            if not success:
                print("❌ Failed to generate prefix audio")
                return None
        else:
            print("ℹ No prefix found (template starts with {name})")

        # Generate suffix audio
        if suffix:
            print(f"\n📝 Suffix: {suffix}")
            suffix_path = os.path.join(self.temp_dir, "suffix.wav")
            success = self.voice_cloner.generate_audio(
                text=suffix,
                output_path=suffix_path,
                language=language,
                show_progress=True
            )
            if not success:
                print("❌ Failed to generate suffix audio")
                return None
        else:
            print("ℹ No suffix found (template ends with {name})")

        print(f"\n✅ Common audio parts generated successfully!")
        return prefix_path, suffix_path

    def generate_name_audio(self, name, language="hi"):
        """
        Generate audio for a single name

        Args:
            name: Name to generate audio for
            language: Language code

        Returns:
            str: Path to generated audio or None if failed
        """
        safe_name = self.sanitize_filename(name)
        output_path = os.path.join(self.temp_dir, f"name_{safe_name}.wav")

        success = self.voice_cloner.generate_audio(
            text=name,
            output_path=output_path,
            language=language,
            show_progress=False
        )

        return output_path if success else None

    def merge_audio_parts(self, prefix_path, name_path, suffix_path, output_path,
                         silence_duration=200):
        """
        Merge prefix + name + suffix audio files

        Args:
            prefix_path: Path to prefix audio (or None)
            name_path: Path to name audio
            suffix_path: Path to suffix audio (or None)
            output_path: Path to save merged audio
            silence_duration: Duration of silence between parts in milliseconds

        Returns:
            bool: True if successful
        """
        try:
            # Create silence
            silence = AudioSegment.silent(duration=silence_duration)

            # Start with empty audio
            merged = AudioSegment.empty()

            # Add prefix if exists
            if prefix_path and os.path.exists(prefix_path):
                prefix_audio = AudioSegment.from_wav(prefix_path)
                merged += prefix_audio + silence

            # Add name audio
            if name_path and os.path.exists(name_path):
                name_audio = AudioSegment.from_wav(name_path)
                merged += name_audio

            # Add suffix if exists
            if suffix_path and os.path.exists(suffix_path):
                suffix_audio = AudioSegment.from_wav(suffix_path)
                merged += silence + suffix_audio

            # Export merged audio
            merged.export(output_path, format="wav")
            return True

        except Exception as e:
            print(f"❌ Error merging audio: {e}")
            return False

    def generate_optimized_batch(self, template, names, language="hi",
                                silence_duration=200):
        """
        Generate optimized batch audio with splitting and merging

        Args:
            template: Template with {name} placeholder
            names: List of names
            language: Language code
            silence_duration: Silence between audio parts (ms)

        Returns:
            dict: Results with success/failed counts and file paths
        """
        print(f"\n{'='*60}")
        print(f"🚀 Optimized Batch Generation")
        print(f"{'='*60}")
        print(f"📊 Total names: {len(names)}")
        print(f"📝 Template: {template}")
        print(f"{'='*60}")

        # Step 1: Generate common audio parts
        common_audio = self.generate_common_audio(template, language)
        if common_audio is None:
            return None

        prefix_path, suffix_path = common_audio

        results = {
            'total': len(names),
            'successful': 0,
            'failed': 0,
            'failed_names': [],
            'file_paths': []
        }

        # Step 2: Generate name audios and merge
        print(f"\n{'='*60}")
        print(f"🎤 Generating Name Audios and Merging")
        print(f"{'='*60}\n")

        with tqdm(total=len(names), desc="Processing names", unit="name") as pbar:
            for name in names:
                name = str(name).strip()

                if not name:
                    continue

                # Generate name audio
                name_audio_path = self.generate_name_audio(name, language)

                if name_audio_path is None:
                    results['failed'] += 1
                    results['failed_names'].append(name)
                    pbar.update(1)
                    continue

                # Merge audio parts
                safe_name = self.sanitize_filename(name)
                output_path = os.path.join(self.output_dir, f"{safe_name}.wav")

                merge_success = self.merge_audio_parts(
                    prefix_path=prefix_path,
                    name_path=name_audio_path,
                    suffix_path=suffix_path,
                    output_path=output_path,
                    silence_duration=silence_duration
                )

                if merge_success:
                    results['successful'] += 1
                    results['file_paths'].append(output_path)
                else:
                    results['failed'] += 1
                    results['failed_names'].append(name)

                # Update progress
                pbar.set_postfix({
                    'Success': results['successful'],
                    'Failed': results['failed']
                })
                pbar.update(1)

        # Print summary
        print(f"\n{'='*60}")
        print(f"✅ Optimized Generation Complete!")
        print(f"{'='*60}")
        print(f"📊 Total: {results['total']}")
        print(f"✓ Successful: {results['successful']}")
        print(f"✗ Failed: {results['failed']}")

        if results['failed_names']:
            print(f"\n⚠ Failed names: {', '.join(results['failed_names'][:10])}")
            if len(results['failed_names']) > 10:
                print(f"   ... and {len(results['failed_names']) - 10} more")

        print(f"\n📁 All files saved in: {self.output_dir}/")
        print(f"💡 Temp files in: {self.temp_dir}/")
        print(f"{'='*60}\n")

        return results

    def generate_from_audio_files(self, prefix_audio_path, suffix_audio_path,
                                  names, language="hi", silence_duration=200):
        """
        Generate batch audio using pre-recorded audio files

        Args:
            prefix_audio_path: Path to prefix audio file (or None)
            suffix_audio_path: Path to suffix audio file (or None)
            names: List of names
            language: Language code
            silence_duration: Silence between parts (ms)

        Returns:
            dict: Results
        """
        print(f"\n{'='*60}")
        print(f"🚀 Generating from Pre-recorded Audio Files")
        print(f"{'='*60}")
        print(f"📊 Total names: {len(names)}")
        print(f"📝 Prefix audio: {prefix_audio_path or 'None'}")
        print(f"📝 Suffix audio: {suffix_audio_path or 'None'}")
        print(f"{'='*60}\n")

        results = {
            'total': len(names),
            'successful': 0,
            'failed': 0,
            'failed_names': [],
            'file_paths': []
        }

        with tqdm(total=len(names), desc="Processing names", unit="name") as pbar:
            for name in names:
                name = str(name).strip()

                if not name:
                    continue

                # Generate name audio
                name_audio_path = self.generate_name_audio(name, language)

                if name_audio_path is None:
                    results['failed'] += 1
                    results['failed_names'].append(name)
                    pbar.update(1)
                    continue

                # Merge audio parts
                safe_name = self.sanitize_filename(name)
                output_path = os.path.join(self.output_dir, f"{safe_name}.wav")

                merge_success = self.merge_audio_parts(
                    prefix_path=prefix_audio_path,
                    name_path=name_audio_path,
                    suffix_path=suffix_audio_path,
                    output_path=output_path,
                    silence_duration=silence_duration
                )

                if merge_success:
                    results['successful'] += 1
                    results['file_paths'].append(output_path)
                else:
                    results['failed'] += 1
                    results['failed_names'].append(name)

                pbar.set_postfix({
                    'Success': results['successful'],
                    'Failed': results['failed']
                })
                pbar.update(1)

        # Print summary
        print(f"\n{'='*60}")
        print(f"✅ Generation Complete!")
        print(f"{'='*60}")
        print(f"📊 Total: {results['total']}")
        print(f"✓ Successful: {results['successful']}")
        print(f"✗ Failed: {results['failed']}")

        if results['failed_names']:
            print(f"\n⚠ Failed names: {', '.join(results['failed_names'][:10])}")

        print(f"\n📁 Files saved in: {self.output_dir}/")
        print(f"{'='*60}\n")

        return results

    def cleanup_temp_files(self):
        """Remove temporary audio files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print(f"🗑️  Cleaned up temp files: {self.temp_dir}")
