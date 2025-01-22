from process_data import extract_text_pymupdf, clean_text, split_into_chunks 
from embed_text import load_model, generate_embeddings
from store_embeddings import store_embeddings, load_embeddings
from retrieve_embeddings import retrieve_similar_chunks
from generate_answer import generate_answer

def main():
    try:
        # File paths
        pdf_path = "sources/BioResoBook.pdf"
        output_file = "sources/embeddings_store" 

        print("Step 1: Extracting and preprocessing text...")
        raw_text = extract_text_pymupdf(pdf_path)
        cleaned_text = clean_text(raw_text)
        chunks = split_into_chunks(cleaned_text)

        print("Step 2: Loading model and generating embeddings...")
        model = load_model()
        embeddings = generate_embeddings(chunks, model)

        print("Step 3: Storing embeddings...")
        store_embeddings(embeddings, chunks, output_file)

        print("Step 4: Loading stored embeddings...")
        index, loaded_chunks = load_embeddings(f"{output_file}.faiss", f"{output_file}_chunks.npy")

        # Query input from the user
        query = input("Enter your query: ")

        print("Step 5: Retrieving relevant chunks...")
        similar_chunks, distances = retrieve_similar_chunks(query, index, loaded_chunks, model)

        # Combine the top relevant chunks into a single context
        context = " ".join(similar_chunks[:3])  # Taking the top 3 chunks

        print("Step 6: Generating an answer...")
        answer = generate_answer(context, query)

        print(f"\nGenerated Answer: {answer}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
