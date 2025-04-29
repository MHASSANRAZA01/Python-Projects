import streamlit as st
import json
import os
from datetime import datetime

# --- Configuration ---
LIBRARY_FILE = "library.json" # File to store library data

# --- Helper Functions ---

def load_library():
    """Loads the library data from the JSON file."""
    if os.path.exists(LIBRARY_FILE):
        try:
            with open(LIBRARY_FILE, 'r') as f:
                # Handle empty or invalid JSON file
                content = f.read()
                if not content:
                    return [] # Return empty list if file is empty
                return json.load(f)
        except json.JSONDecodeError:
            st.error(f"Error reading {LIBRARY_FILE}. It might be corrupted. Starting with an empty library.")
            return []
        except Exception as e:
            st.error(f"An unexpected error occurred while loading the library: {e}")
            return []
    else:
        return [] # Return empty list if file doesn't exist

def save_library(library_data):
    """Saves the library data to the JSON file."""
    try:
        with open(LIBRARY_FILE, 'w') as f:
            json.dump(library_data, f, indent=4)
    except Exception as e:
        st.error(f"An error occurred while saving the library: {e}")

def display_book(book, index):
    """Formats and displays a single book's details."""
    read_status = "Read" if book.get('read_status', False) else "Unread"
    # Use get with default values for robustness against missing keys
    title = book.get('title', 'N/A')
    author = book.get('author', 'N/A')
    year = book.get('publication_year', 'N/A')
    genre = book.get('genre', 'N/A')

    st.markdown(f"""
    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 10px;">
        <strong>{index}. {title}</strong> by <em>{author}</em> ({year})<br>
        Genre: {genre}<br>
        Status: {read_status}
    </div>
    """, unsafe_allow_html=True)

# --- Initialize Session State ---
if 'library' not in st.session_state:
    st.session_state.library = load_library()

# --- Streamlit App UI ---
st.set_page_config(page_title="Personal Library Manager", layout="wide")

st.title("📚 Personal Library Manager")
st.markdown("Manage your book collection with ease.")

# --- Sidebar Menu ---
st.sidebar.header("Menu")
menu_choice = st.sidebar.radio(
    "Choose an action:",
    ("Add Book", "Remove Book", "Search Books", "Display All Books", "Statistics")
)

# --- Main Content Area ---

# --- Add Book ---
if menu_choice == "Add Book":
    st.header("Add a New Book")
    with st.form("add_book_form", clear_on_submit=True):
        title = st.text_input("Title *", key="add_title")
        author = st.text_input("Author *", key="add_author")
        # Use number input for year, set reasonable min/max
        current_year = datetime.now().year
        year = st.number_input("Publication Year", min_value=0, max_value=current_year, step=1, key="add_year", value=current_year)
        genre = st.text_input("Genre", key="add_genre")
        read_status = st.checkbox("Mark as Read?", key="add_read_status")

        submitted = st.form_submit_button("Add Book")
        if submitted:
            if not title or not author:
                st.warning("Title and Author are required fields.")
            else:
                new_book = {
                    "title": title.strip(),
                    "author": author.strip(),
                    "publication_year": year,
                    "genre": genre.strip(),
                    "read_status": read_status
                }
                # Check for duplicates (optional, based on title and author)
                is_duplicate = any(
                    b['title'].lower() == new_book['title'].lower() and
                    b['author'].lower() == new_book['author'].lower()
                    for b in st.session_state.library
                )
                if is_duplicate:
                    st.warning(f"A book with the title '{title}' by '{author}' already exists.")
                else:
                    st.session_state.library.append(new_book)
                    save_library(st.session_state.library)
                    st.success(f"Book '{title}' added successfully!")
                    # Clear form fields explicitly if needed (though clear_on_submit helps)
                    # st.session_state.add_title = ""
                    # ... reset other keys if necessary


# --- Remove Book ---
elif menu_choice == "Remove Book":
    st.header("Remove a Book")
    if not st.session_state.library:
        st.info("Your library is currently empty. Add some books first!")
    else:
        # Create a list of titles for the selectbox, adding index for uniqueness if needed
        book_titles = [f"{i+1}. {book['title']} by {book['author']}" for i, book in enumerate(st.session_state.library)]
        book_to_remove_display = st.selectbox("Select the book to remove:", options=[""] + book_titles)

        if book_to_remove_display:
            # Extract the index from the selected string
            try:
                selected_index = int(book_to_remove_display.split('.')[0]) - 1
                book_title_to_remove = st.session_state.library[selected_index]['title'] # Get title for confirmation

                if st.button(f"Confirm Removal of '{book_title_to_remove}'"):
                    removed_book = st.session_state.library.pop(selected_index)
                    save_library(st.session_state.library)
                    st.success(f"Book '{removed_book['title']}' removed successfully!")
                    st.rerun() # Rerun to update the selectbox
            except (IndexError, ValueError):
                st.error("Invalid selection. Please choose a book from the list.")


# --- Search Books ---
elif menu_choice == "Search Books":
    st.header("Search Your Library")
    if not st.session_state.library:
        st.info("Your library is currently empty. Add some books first!")
    else:
        search_by = st.radio("Search by:", ("Title", "Author"), horizontal=True)
        search_term = st.text_input(f"Enter {search_by} to search for:", key="search_term").strip().lower()

        if search_term:
            results = []
            if search_by == "Title":
                results = [book for book in st.session_state.library if search_term in book.get('title', '').lower()]
            elif search_by == "Author":
                results = [book for book in st.session_state.library if search_term in book.get('author', '').lower()]

            st.subheader("Search Results")
            if results:
                for i, book in enumerate(results):
                    display_book(book, i + 1)
            else:
                st.info(f"No books found matching '{search_term}' by {search_by}.")

# --- Display All Books ---
elif menu_choice == "Display All Books":
    st.header("Your Library Collection")
    if not st.session_state.library:
        st.info("Your library is currently empty. Add some books first!")
    else:
        st.write(f"Total books: {len(st.session_state.library)}")
        # Sort books alphabetically by title (optional)
        sorted_library = sorted(st.session_state.library, key=lambda x: x.get('title', '').lower())
        for i, book in enumerate(sorted_library):
            display_book(book, i + 1)

# --- Statistics ---
elif menu_choice == "Statistics":
    st.header("Library Statistics")
    total_books = len(st.session_state.library)

    if total_books == 0:
        st.info("Your library is empty. No statistics to display yet.")
    else:
        read_books = sum(1 for book in st.session_state.library if book.get('read_status', False))
        try:
            percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
        except ZeroDivisionError:
             percentage_read = 0

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total Books", value=total_books)
        with col2:
            st.metric(label="Books Read", value=f"{read_books} ({percentage_read:.1f}%)")

        # Optional: Add more stats like books per genre, etc.
        if total_books > 0:
            st.subheader("Books by Read Status")
            status_counts = {"Read": read_books, "Unread": total_books - read_books}
            st.bar_chart(status_counts)


# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.info(f"Library data is saved to `{LIBRARY_FILE}`.")
