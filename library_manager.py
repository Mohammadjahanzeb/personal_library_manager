import streamlit as st
import json

# Load & save library data
def load_library():
    try:
        with open("library.json", "r") as file:
            content = file.read().strip()  # Remove extra spaces/newlines
            return json.loads(content) if content else []  # Return empty list if file is empty
    except (FileNotFoundError, json.JSONDecodeError):  # Handle missing or corrupt file
        return []

def save_library():
    with open("library.json", "w") as file:
        json.dump(library, file, indent=4)

# Initialize library
library = load_library()

st.title("Personal Library Manager")

menu = st.sidebar.radio("Select an option", ["View Library", "Add Book", "Remove Book", "Search Book", "Save and Exit"])

# View Library
if menu == "View Library":
    st.sidebar.title("Your Library")
    if library:
        st.table(library)
    else:
        st.write("No books in your library. Add some books!")

# Add Book
elif menu == "Add Book":
    st.sidebar.title("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Year", min_value=2022, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Mark as Read")

    if st.button("Add Book"):
        if title and author:
            library.append({"title": title, "author": author, "year": year, "genre": genre, "read_status": read_status})
            save_library()  # Save changes
            st.success("Book added successfully!")
            st.rerun()  # Refresh app to update UI
        else:
            st.error("Please enter both title and author!")

# Remove Book
elif menu == "Remove Book":
    st.sidebar.title("Remove a Book")
    book_titles = [book['title'] for book in library]

    if book_titles:
        selected_book = st.selectbox("Select a book to remove", book_titles)
        if st.button("Remove Book"):
            for book in library:
                if book["title"] == selected_book:
                    library.remove(book)  # Modify list in place
                    break  # Stop loop after removing first match
            save_library()  # Save changes
            st.success("Book removed successfully!")
            st.rerun()
    else:
        st.warning("No books in your library. Add some books!")

# Search Book
elif menu == "Search Book":
    st.sidebar.title("Search a Book")
    search_term = st.text_input("Enter title or author name")

    if st.button("Search"):
        results = [
            book for book in library 
            if search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower()
        ]
        if results:
            st.table(results)
        else:
            st.warning("No book found!")

# Save and Exit
elif menu == "Save and Exit":
    save_library()
    st.success("Library saved successfully!")






