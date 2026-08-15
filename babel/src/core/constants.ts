/**
 * The immutable facts of the Library, as given by Borges.
 *
 * "...each book is of four hundred and ten pages; each page, of forty lines,
 *  each line, of some eighty letters which are black in color."
 * "The orthographical symbols are twenty-five in number."
 * "There are five shelves for each of the hexagon's walls; each shelf contains
 *  thirty-two books of uniform format."
 */

/** Lines per page. */
export const LINES = 40;
/** Characters per line ("some eighty letters"). */
export const COLS = 80;
/** Characters per page. */
export const PAGE_CHARS = LINES * COLS; // 3200
/** Pages per book. */
export const PAGES = 410;
/** Characters per book. */
export const BOOK_CHARS = PAGES * PAGE_CHARS; // 1,312,000

/** Walls of a hexagon that carry shelves ("all the sides except two"). */
export const WALLS = 4;
/** Shelves per shelf-wall ("five long shelves per side"). */
export const SHELVES = 5;
/** Books per shelf. */
export const VOLUMES = 32;
/** Books per hexagon. */
export const BOOKS_PER_HEX = WALLS * SHELVES * VOLUMES; // 640
/** Distinct shelf positions a book can occupy inside a hexagon. */
export const SLOTS = BOOKS_PER_HEX;

/**
 * Master seed of this universe. Changing it would quietly replace every book
 * in the Library with a different one, so: don't.
 */
export const GLOBAL_SEED = "borges-1941-the-total-library";
