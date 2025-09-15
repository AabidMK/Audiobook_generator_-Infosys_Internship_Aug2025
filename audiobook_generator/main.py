import asyncio
import os
from audiobook_generator import AudiobookGenerator

async def main():
    """Test the complete audiobook generation pipeline"""
    
    # Your test files
    test_files = [
        # Add more files here
    ]
    
    generator = AudiobookGenerator()
    
    for file_path in test_files:
        if os.path.isfile(file_path):
            try:
                result_file = await generator.generate_audiobook_text(file_path)
                print(f"🎉 Success! AudioBook text ready: {result_file}")
            except Exception as e:
                print(f"❌ Failed processing {file_path}: {e}")
        else:
            print(f"⚠️ File not found: {file_path}")

if __name__ == "__main__":
    asyncio.run(main())
