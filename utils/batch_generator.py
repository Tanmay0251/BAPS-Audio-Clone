"""
Batch Audio Generator for Google Colab
Processes names from sheets/CSVs and generates personalized audio files
"""

import os
import pandas as pd
import re
from datetime import datetime
from IPython.display import display, HTML
from tqdm.auto import tqdm


class BatchAudioGenerator:
    def __init__(self, voice_cloner, template_text, output_dir="generated_audios"):
        """
        Initialize batch audio generator

        Args:
            voice_cloner: VoiceCloner instance
            template_text: Hindi text template with {name} placeholder
                          Example: "नमस्ते {name}, आपका स्वागत है।"
            output_dir: Directory to save generated audio files
        """
        self.voice_cloner = voice_cloner
        self.template_text = template_text
        self.output_dir = output_dir

        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"📁 Output directory: {self.output_dir}")

    def sanitize_filename(self, name):
        """Convert name to safe filename"""
        # Remove special characters and spaces
        safe_name = re.sub(r'[^\w\s-]', '', name)
        safe_name = re.sub(r'\s+', '_', safe_name)
        return safe_name[:100]  # Limit filename length

    def load_names_from_sheet(self, sheet_path_or_df, name_column="Name", sheet_name=None):
        """
        Load names from Excel/CSV or DataFrame

        Args:
            sheet_path_or_df: Path to file or pandas DataFrame
            name_column: Name of the column containing names
            sheet_name: Sheet name for Excel files (default: first sheet)

        Returns:
            list: List of names
        """
        # If already a DataFrame
        if isinstance(sheet_path_or_df, pd.DataFrame):
            df = sheet_path_or_df
        else:
            # Read from file
            try:
                if sheet_path_or_df.endswith('.csv'):
                    df = pd.read_csv(sheet_path_or_df)
                elif sheet_path_or_df.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(sheet_path_or_df, sheet_name=sheet_name)
                else:
                    raise ValueError("Unsupported file format. Use .csv, .xlsx, or .xls")
            except Exception as e:
                print(f"❌ Error reading sheet: {e}")
                return []

        # Validate name column exists
        if name_column not in df.columns:
            print(f"❌ Column '{name_column}' not found in sheet.")
            print(f"Available columns: {', '.join(df.columns)}")
            return []

        # Get names and remove empty/null values
        names = df[name_column].dropna().astype(str).str.strip().tolist()
        names = [n for n in names if n]  # Remove empty strings

        return names

    def generate_from_names(self, names, add_timestamp=True, language="hi"):
        """
        Generate audio files for a list of names

        Args:
            names: List of names
            add_timestamp: Add timestamp to filename
            language: Language code (default: "hi" for Hindi)

        Returns:
            dict: Results with success/failed counts and file paths
        """
        total_names = len(names)
        print(f"\n{'='*60}")
        print(f"🎬 Starting Batch Audio Generation")
        print(f"{'='*60}")
        print(f"📊 Total names: {total_names}")
        print(f"📝 Template: {self.template_text}")
        print(f"{'='*60}\n")

        results = {
            'total': total_names,
            'successful': 0,
            'failed': 0,
            'failed_names': [],
            'file_paths': []
        }

        # Progress bar for Colab
        with tqdm(total=total_names, desc="Generating audio", unit="name") as pbar:
            for name in names:
                name = str(name).strip()

                if not name:
                    continue

                # Replace placeholder with name
                personalized_text = self.template_text.replace("{name}", name)

                # Create output filename
                safe_name = self.sanitize_filename(name)
                if add_timestamp:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_filename = f"{safe_name}_{timestamp}.mp3"
                else:
                    output_filename = f"{safe_name}.mp3"

                output_path = os.path.join(self.output_dir, output_filename)

                # Generate audio as MP3
                success = self.voice_cloner.generate_audio(
                    text=personalized_text,
                    output_path=output_path,
                    language=language,
                    show_progress=False,
                    output_format="mp3"
                )

                if success:
                    results['successful'] += 1
                    results['file_paths'].append(output_path)
                else:
                    results['failed'] += 1
                    results['failed_names'].append(name)

                # Update progress bar
                pbar.set_postfix({'Success': results['successful'], 'Failed': results['failed']})
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
            if len(results['failed_names']) > 10:
                print(f"   ... and {len(results['failed_names']) - 10} more")

        print(f"\n📁 All files saved in: {self.output_dir}/")
        print(f"{'='*60}\n")

        return results

    def generate_from_sheet(self, sheet_path_or_df, name_column="Name", sheet_name=None, add_timestamp=True):
        """
        Generate audio files for all names in the sheet

        Args:
            sheet_path_or_df: Path to Excel/CSV file or pandas DataFrame
            name_column: Name of the column containing names
            sheet_name: Sheet name for Excel files (default: first sheet)
            add_timestamp: Add timestamp to filename

        Returns:
            dict: Results with success/failed counts and file paths
        """
        # Load names
        names = self.load_names_from_sheet(sheet_path_or_df, name_column, sheet_name)

        if not names:
            print("❌ No names found to process")
            return None

        # Generate audio
        return self.generate_from_names(names, add_timestamp=add_timestamp)

    def generate_single(self, name, custom_text=None, output_filename=None):
        """
        Generate audio for a single name (useful for testing)

        Args:
            name: Name to use in the template
            custom_text: Custom template (optional, uses default if not provided)
            output_filename: Custom output filename (optional)

        Returns:
            str: Path to generated audio file or None if failed
        """
        text = custom_text if custom_text else self.template_text
        personalized_text = text.replace("{name}", name)

        if output_filename is None:
            safe_name = self.sanitize_filename(name)
            output_filename = f"{safe_name}.mp3"

        output_path = os.path.join(self.output_dir, output_filename)

        print(f"🎤 Generating audio for: {name}")
        success = self.voice_cloner.generate_audio(
            personalized_text,
            output_path,
            show_progress=True,
            output_format="mp3"
        )

        return output_path if success else None
