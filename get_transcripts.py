import asyncio
import os
import platform
from granola_client import GranolaClient, GranolaAuthError, DocumentsResponse

async def main():
    client = None
    try:
        api_token = "your-api-token" # Replace or use macOS auto-retrieval

        if platform.system() == "Darwin" and api_token == "your-api-token":
            print("Attempting to initialize client with automatic token retrieval (macOS)...")
            client = GranolaClient()
        else:
            if api_token == "your-api-token":
                print("Placeholder token detected. Please set a real token or run on macOS for auto-retrieval.")
                return
            client = GranolaClient(token=api_token)

        # Get documents
        print("\nRetrieving documents...")
        documents_response: DocumentsResponse = await client.get_documents()
        
        for doc in documents_response.docs:
            if os.path.exists(f"transcripts/{doc.title}__{doc.document_id}.txt"):
                print(f"Transcript already exists for {doc.title}")
                continue
            
            try:
                transcript_segments = await client.get_document_transcript(doc.document_id)
                
                # Only create the file if we successfully got the transcript
                os.makedirs("transcripts", exist_ok=True)
                with open(f"transcripts/{doc.title}__{doc.document_id}.txt", "w") as f:
                    for segment in transcript_segments:
                        f.write(segment.source + ": " + segment.text + "\n")

                print(f"Transcript stored to {doc.title}__{doc.document_id}.txt")
            except Exception as e:
                print(f"Failed to get transcript for {doc.title}: {e}")
                continue

    except GranolaAuthError as e:
        print(f"Authentication Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if client:
            await client.close()


if __name__ == "__main__":
    asyncio.run(main())