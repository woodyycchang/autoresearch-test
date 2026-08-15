/**
 * The flat surfaces of the experience: HUD, the opened volume, the seek
 * panel, the start screen, help, and the long fall. Plain DOM; the Library
 * needs no framework.
 */

import { PAGES, PAGE_CHARS, COLS, LINES } from "../core/constants";
import { transliterate } from "../core/alphabet";
import { Book, pageText, SeekMode, SeekResult } from "../core/library";

export interface UICallbacks {
  onSeek(text: string, mode: SeekMode, copy: number): SeekResult | string;
  onTravel(): void;
  onCloseBook(): void;
  onResume(): void;
  onWake(): void;
  onShare(): string | null;
}

const WALL_NAMES = ["southeast", "southwest", "northwest", "northeast"];

export function describeWall(w: number): string {
  return WALL_NAMES[w] ?? `wall ${w}`;
}

export class UI {
  private cb: UICallbacks;
  root: HTMLElement;

  private hudName!: HTMLElement;
  private hudFloor!: HTMLElement;
  private hudSteps!: HTMLElement;
  private prompt!: HTMLElement;
  private toastEl!: HTMLElement;
  private toastTimer = 0;

  private bookView!: HTMLElement;
  private bookSpine!: HTMLElement;
  private bookWhere!: HTMLElement;
  private bookPageText!: HTMLElement;
  private pageSlider!: HTMLInputElement;
  private pageNum!: HTMLInputElement;
  private pageLabel!: HTMLElement;
  private openBookRef: Book | null = null;
  private currentPage = 0;
  private highlight: { page: number; start: number; length: number } | null = null;

  private seekPanel!: HTMLElement;
  private seekText!: HTMLTextAreaElement;
  private seekPreview!: HTMLElement;
  private seekNotes!: HTMLElement;
  private seekResultEl!: HTMLElement;
  private seekErrorEl!: HTMLElement;
  private copyIndex = 0;
  lastSeek: SeekResult | null = null;

  private startOverlay!: HTMLElement;
  private helpOverlay!: HTMLElement;
  private fallOverlay!: HTMLElement;
  private fadeEl!: HTMLElement;

  constructor(root: HTMLElement, cb: UICallbacks) {
    this.cb = cb;
    this.root = root;
    this.build();
  }

  // ------------------------------------------------------------- structure

  private build(): void {
    this.root.insertAdjacentHTML(
      "beforeend",
      `
      <div id="vignette"></div>
      <div id="crosshair"></div>
      <div id="hud">
        <div class="hexname" id="hudName">—</div>
        <div id="hudFloor"></div>
        <div id="hudSteps"></div>
      </div>
      <div id="hudButtons">
        <button id="btnSeek" title="Seek a text (F)">Seek</button>
        <button id="btnHelp" title="Help (H)">Help</button>
        <button id="btnMute" title="Sound (M)">Sound</button>
      </div>
      <div id="prompt" class="hidden"></div>
      <div id="toast" style="opacity:0"></div>
      <div id="fade"></div>
      `,
    );
    this.hudName = document.getElementById("hudName")!;
    this.hudFloor = document.getElementById("hudFloor")!;
    this.hudSteps = document.getElementById("hudSteps")!;
    this.prompt = document.getElementById("prompt")!;
    this.toastEl = document.getElementById("toast")!;
    this.fadeEl = document.getElementById("fade")!;

    this.buildBookView();
    this.buildSeekPanel();
    this.buildOverlays();
  }

  private buildBookView(): void {
    this.root.insertAdjacentHTML(
      "beforeend",
      `
      <div id="bookView" class="hidden">
        <div class="volume">
          <header>
            <span class="spine-title" id="bookSpine"></span>
            <span class="where" id="bookWhere"></span>
            <button class="closeBtn" id="bookClose">return to shelf (esc)</button>
          </header>
          <div id="pageWrap"><pre id="pageText"></pre></div>
          <footer>
            <button id="pagePrev">previous</button>
            <input id="pageSlider" type="range" min="1" max="${PAGES}" value="1" />
            <button id="pageNext">next</button>
            <span>page <input id="pageNum" type="number" min="1" max="${PAGES}" value="1" /> of ${PAGES}</span>
            <span id="pageLabel"></span>
            <button id="copyPage">copy page</button>
            <button id="copyAddr">copy address</button>
          </footer>
        </div>
      </div>
      `,
    );
    this.bookView = document.getElementById("bookView")!;
    this.bookSpine = document.getElementById("bookSpine")!;
    this.bookWhere = document.getElementById("bookWhere")!;
    this.bookPageText = document.getElementById("pageText")!;
    this.pageSlider = document.getElementById("pageSlider") as HTMLInputElement;
    this.pageNum = document.getElementById("pageNum") as HTMLInputElement;
    this.pageLabel = document.getElementById("pageLabel")!;

    document.getElementById("bookClose")!.addEventListener("click", () => this.cb.onCloseBook());
    document.getElementById("pagePrev")!.addEventListener("click", () => this.showPage(this.currentPage - 1));
    document.getElementById("pageNext")!.addEventListener("click", () => this.showPage(this.currentPage + 1));
    this.pageSlider.addEventListener("input", () => this.showPage(parseInt(this.pageSlider.value, 10) - 1));
    this.pageNum.addEventListener("change", () => this.showPage(parseInt(this.pageNum.value, 10) - 1));
    document.getElementById("copyPage")!.addEventListener("click", () => {
      if (!this.openBookRef) return;
      navigator.clipboard?.writeText(pageText(this.openBookRef, this.currentPage)).catch(() => {});
      this.toast("page copied");
    });
    document.getElementById("copyAddr")!.addEventListener("click", () => {
      if (!this.openBookRef) return;
      const b = this.openBookRef;
      const text = `hexagon ${b.hexName}, floor ${b.location.coord.f}, ${describeWall(b.location.wall)} wall, shelf ${b.location.shelf + 1}, volume ${b.location.volume + 1}, page ${this.currentPage + 1}`;
      navigator.clipboard?.writeText(text).catch(() => {});
      this.toast("address copied: " + text);
    });
  }

  private buildSeekPanel(): void {
    this.root.insertAdjacentHTML(
      "beforeend",
      `
      <div id="seekPanel" class="hidden">
        <h3>Seek a text</h3>
        <div class="sub">Name any words, and the Library will show the shelf that has always held them.</div>
        <textarea id="seekText" placeholder="oh time thy pyramids" spellcheck="false"></textarea>
        <div id="seekPreview" class="hidden"></div>
        <div id="seekNotes"></div>
        <div class="modes">
          <label><input type="radio" name="seekMode" value="context" checked /> amid the usual chaos</label>
          <label><input type="radio" name="seekMode" value="alone" /> alone in a blank book</label>
        </div>
        <div class="row">
          <button id="seekGo">Seek</button>
          <button id="seekAnother" class="ghost hidden">another copy</button>
          <button id="seekShare" class="ghost hidden">copy link</button>
        </div>
        <div id="seekError" class="hidden"></div>
        <div id="seekResult" class="hidden"></div>
      </div>
      `,
    );
    this.seekPanel = document.getElementById("seekPanel")!;
    this.seekText = document.getElementById("seekText") as HTMLTextAreaElement;
    this.seekPreview = document.getElementById("seekPreview")!;
    this.seekNotes = document.getElementById("seekNotes")!;
    this.seekResultEl = document.getElementById("seekResult")!;
    this.seekErrorEl = document.getElementById("seekError")!;

    this.seekText.addEventListener("input", () => {
      this.copyIndex = 0;
      this.updatePreview();
    });
    document.getElementById("seekGo")!.addEventListener("click", () => this.runSeek());
    document.getElementById("seekAnother")!.addEventListener("click", () => {
      this.copyIndex++;
      this.runSeek();
    });
    document.getElementById("seekShare")!.addEventListener("click", () => {
      const url = this.cb.onShare();
      if (url) {
        navigator.clipboard?.writeText(url).catch(() => {});
        this.toast("link copied — it leads to this very book");
      }
    });
  }

  private buildOverlays(): void {
    this.root.insertAdjacentHTML(
      "beforeend",
      `
      <div id="startOverlay" class="overlay">
        <div class="sheet">
          <h1>The Library of Babel</h1>
          <h2>after the story by Jorge Luis Borges (1941)</h2>
          <p class="quote">"The universe (which others call the Library) is composed of an indefinite and perhaps infinite number of hexagonal galleries…"</p>
          <p>You wake in a hexagon among endless hexagons. Four of its walls carry
          twenty shelves; the shelves carry six hundred forty books; the books carry
          every combination of twenty-five symbols — which is to say, everything:
          your name, this sentence, the true account of your death, and the
          catalogue of catalogues. A vestibule on either side leads to the next
          gallery; a spiral stair climbs and sinks forever; a mirror faithfully
          duplicates appearances.</p>
          <ul class="keys">
            <li><kbd>W A S D</kbd> walk</li>
            <li><kbd>mouse</kbd> / <kbd>arrows</kbd> look</li>
            <li><kbd>E</kbd> take / return a book</li>
            <li><kbd>F</kbd> seek a text</li>
            <li><kbd>space</kbd> hop (mind the railing)</li>
            <li><kbd>shift</kbd> hurry</li>
            <li><kbd>H</kbd> help &nbsp; <kbd>M</kbd> sound</li>
          </ul>
          <p style="margin-top:14px"><label><input type="checkbox" id="qualityLow" /> economy mode (slower machines)</label></p>
          <button class="primary" id="enterBtn">Enter the Library</button>
        </div>
      </div>
      <div id="helpOverlay" class="overlay hidden">
        <div class="sheet">
          <h1>A traveler's notes</h1>
          <p>Each hexagon is identical: twenty shelves, thirty-two books to a shelf,
          410 pages to a book, forty lines to a page, some eighty characters to a
          line. The letters on a spine do not prefigure what the pages will say.
          The light is insufficient, incessant.</p>
          <p>Walk <em>east</em> or <em>west</em> and the corridor never ends. The spiral stairs in
          each vestibule sink and soar to other floors. The shaft at the center of
          every gallery is bottomless: the railing is very low, and the Library
          does not catch those who lean too far.</p>
          <p><strong>Seek</strong> (<kbd>F</kbd>) computes the exact hexagon, wall, shelf, volume and
          page of any text you can type — it is not placed there for you; it has
          been there all along. The same words always lead to the same book.</p>
          <ul class="keys">
            <li><kbd>W A S D</kbd> walk</li>
            <li><kbd>mouse / arrows</kbd> look</li>
            <li><kbd>E</kbd> take / return a book</li>
            <li><kbd>F</kbd> seek</li>
            <li><kbd>space</kbd> hop</li>
            <li><kbd>esc</kbd> release the mouse</li>
          </ul>
          <button class="primary" id="helpClose">Return</button>
        </div>
      </div>
      <div id="fallOverlay" class="overlay hidden">
        <div class="sheet">
          <h1 id="fallTitle">You fall.</h1>
          <p id="fallText">The shaft has no bottom: your body will sink for centuries past
          hexagons identical to the ones you knew. Somewhere below, the air will
          claim what the Library no longer needs.</p>
          <button class="primary" id="wakeBtn">Wake on a remote floor</button>
        </div>
      </div>
      `,
    );
    this.startOverlay = document.getElementById("startOverlay")!;
    this.helpOverlay = document.getElementById("helpOverlay")!;
    this.fallOverlay = document.getElementById("fallOverlay")!;
    document.getElementById("helpClose")!.addEventListener("click", () => {
      this.helpOverlay.classList.add("hidden");
      this.cb.onResume();
    });
    document.getElementById("wakeBtn")!.addEventListener("click", () => this.cb.onWake());
  }

  // ---------------------------------------------------------------- pieces

  bindStart(onEnter: (lowQuality: boolean) => void): void {
    document.getElementById("enterBtn")!.addEventListener("click", () => {
      const low = (document.getElementById("qualityLow") as HTMLInputElement).checked;
      this.startOverlay.classList.add("hidden");
      onEnter(low);
    });
  }

  startHidden(): boolean {
    return this.startOverlay.classList.contains("hidden");
  }

  setHud(hexName: string, floor: number, steps: number, far: boolean): void {
    this.hudName.textContent = hexName;
    this.hudFloor.textContent = `floor ${floor.toLocaleString("en-US")}`;
    this.hudSteps.textContent = far
      ? "unfathomably far from your first hexagon"
      : steps === 0
        ? "the hexagon of your first waking"
        : `${Math.abs(steps).toLocaleString("en-US")} ${steps > 0 ? "east" : "west"} of your first hexagon`;
  }

  setPrompt(html: string | null): void {
    if (html === null) {
      this.prompt.classList.add("hidden");
    } else {
      this.prompt.innerHTML = html;
      this.prompt.classList.remove("hidden");
    }
  }

  toast(text: string, ms = 2600): void {
    this.toastEl.textContent = text;
    this.toastEl.style.opacity = "1";
    window.clearTimeout(this.toastTimer);
    this.toastTimer = window.setTimeout(() => {
      this.toastEl.style.opacity = "0";
    }, ms);
  }

  fade(dark: boolean): void {
    this.fadeEl.classList.toggle("dark", dark);
  }

  // ------------------------------------------------------------- the book

  openBook(book: Book, opts?: { page?: number; highlight?: { page: number; start: number; length: number } }): void {
    this.openBookRef = book;
    this.highlight = opts?.highlight ?? null;
    this.bookSpine.textContent = book.spine;
    const loc = book.location;
    this.bookWhere.textContent =
      `hexagon ${book.hexName} · floor ${loc.coord.f.toLocaleString("en-US")} · ` +
      `${describeWall(loc.wall)} wall · shelf ${loc.shelf + 1} of 5 · volume ${loc.volume + 1} of 32`;
    this.bookView.classList.remove("hidden");
    this.showPage(opts?.page ?? 0);
  }

  closeBook(): void {
    this.bookView.classList.add("hidden");
    this.openBookRef = null;
    this.highlight = null;
  }

  bookIsOpen(): boolean {
    return !this.bookView.classList.contains("hidden");
  }

  showPage(page: number): void {
    if (!this.openBookRef) return;
    page = Math.max(0, Math.min(PAGES - 1, page));
    this.currentPage = page;
    const text = pageText(this.openBookRef, page);
    if (this.highlight && this.highlight.page === page) {
      const startInPage = this.highlight.start - page * PAGE_CHARS;
      const from = Math.max(0, startInPage);
      const to = Math.min(PAGE_CHARS, startInPage + this.highlight.length);
      this.bookPageText.innerHTML =
        wrapLines(escapeHtml(text.slice(0, from))) +
        "<mark>" +
        wrapLines(escapeHtml(text.slice(from, to)), from) +
        "</mark>" +
        wrapLines(escapeHtml(text.slice(to)), to);
    } else {
      this.bookPageText.textContent = withNewlines(text);
    }
    this.pageSlider.value = String(page + 1);
    this.pageNum.value = String(page + 1);
    const hl = this.highlight;
    this.pageLabel.textContent = hl
      ? hl.page === page
        ? "— the sought page"
        : `— sought text on page ${hl.page + 1}`
      : "";
  }

  get openedBook(): Book | null {
    return this.openBookRef;
  }

  get shownPage(): number {
    return this.currentPage;
  }

  // ------------------------------------------------------------- the seek

  toggleSeek(force?: boolean): boolean {
    const show = force ?? this.seekPanel.classList.contains("hidden");
    this.seekPanel.classList.toggle("hidden", !show);
    if (show) {
      this.updatePreview();
      setTimeout(() => this.seekText.focus(), 30);
    }
    return show;
  }

  seekIsOpen(): boolean {
    return !this.seekPanel.classList.contains("hidden");
  }

  setSeekText(text: string, mode: SeekMode): void {
    this.seekText.value = text;
    const radio = document.querySelector<HTMLInputElement>(`input[name=seekMode][value=${mode}]`);
    if (radio) radio.checked = true;
    this.updatePreview();
  }

  private updatePreview(): void {
    const raw = this.seekText.value;
    if (!raw) {
      this.seekPreview.classList.add("hidden");
      this.seekNotes.textContent = "";
      return;
    }
    const t = transliterate(raw);
    this.seekPreview.classList.remove("hidden");
    this.seekPreview.textContent = t.text.length ? t.text : "(nothing survives)";
    const notes: string[] = [];
    if (t.substituted.length) notes.push("the librarians transcribe: " + t.substituted.join(", "));
    if (t.dropped.length) notes.push("no symbol exists for: " + t.dropped.join(" "));
    notes.push(`${t.text.length.toLocaleString("en-US")} characters`);
    this.seekNotes.textContent = notes.join(" · ");
  }

  private runSeek(): void {
    const mode = (document.querySelector<HTMLInputElement>("input[name=seekMode]:checked")?.value ?? "context") as SeekMode;
    const res = this.cb.onSeek(this.seekText.value, mode, this.copyIndex);
    if (typeof res === "string") {
      this.seekErrorEl.textContent = res;
      this.seekErrorEl.classList.remove("hidden");
      this.seekResultEl.classList.add("hidden");
      document.getElementById("seekAnother")!.classList.add("hidden");
      document.getElementById("seekShare")!.classList.add("hidden");
      this.lastSeek = null;
      return;
    }
    this.lastSeek = res;
    this.seekErrorEl.classList.add("hidden");
    this.showSeekResult(res);
  }

  showSeekResult(res: SeekResult): void {
    this.seekResultEl.classList.remove("hidden");
    document.getElementById("seekAnother")!.classList.remove("hidden");
    document.getElementById("seekShare")!.classList.remove("hidden");
    this.seekResultEl.innerHTML =
      `It stands where it has always stood:<br/>` +
      `<span class="addr" id="seekAddr"></span><br/>` +
      `floor <span id="seekFloor"></span> · ${describeWall(res.location.wall)} wall · shelf ${res.location.shelf + 1} · volume ${res.location.volume + 1} · page ${res.page + 1}` +
      `${res.copy > 0 ? `<br/>(copy ${res.copy + 1} — other volumes hold these words too)` : ""}` +
      `<div class="row"><button id="travelBtn">Travel there</button></div>`;
    // Fill names safely (they contain no HTML, but be tidy).
    (document.getElementById("seekFloor")!).textContent = res.location.coord.f.toLocaleString("en-US");
    document.getElementById("travelBtn")!.addEventListener("click", () => this.cb.onTravel());
    return;
  }

  setSeekAddr(name: string): void {
    const el = document.getElementById("seekAddr");
    if (el) el.textContent = `hexagon ${name}`;
  }

  // ------------------------------------------------------------- overlays

  showHelp(show: boolean): void {
    this.helpOverlay.classList.toggle("hidden", !show);
  }

  helpIsOpen(): boolean {
    return !this.helpOverlay.classList.contains("hidden");
  }

  showFall(show: boolean): void {
    this.fallOverlay.classList.toggle("hidden", !show);
  }

  setMuteLabel(muted: boolean): void {
    document.getElementById("btnMute")!.textContent = muted ? "Sound: off" : "Sound: on";
  }

  bindButtons(handlers: { seek(): void; help(): void; mute(): void }): void {
    document.getElementById("btnSeek")!.addEventListener("click", handlers.seek);
    document.getElementById("btnHelp")!.addEventListener("click", handlers.help);
    document.getElementById("btnMute")!.addEventListener("click", handlers.mute);
  }
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/** Insert newlines so each 80-character line stands alone. */
function withNewlines(page: string): string {
  const lines: string[] = [];
  for (let l = 0; l < LINES; l++) lines.push(page.slice(l * COLS, (l + 1) * COLS));
  return lines.join("\n");
}

/**
 * Like withNewlines but for a fragment that starts mid-page at `offset`
 * characters: keeps the 80-column rhythm across <mark> boundaries.
 */
function wrapLines(fragment: string, offset = 0): string {
  let out = "";
  let col = offset % COLS;
  for (const ch of fragment) {
    out += ch;
    col++;
    if (col === COLS) {
      out += "\n";
      col = 0;
    }
  }
  return out;
}
