/* Original educational demo. No radio, NFC, storage or network access. */
#include <furi.h>
#include <gui/gui.h>
#include <input/input.h>
#include <stdio.h>

typedef struct {
    FuriMutex* mutex;
    uint8_t target;
    uint8_t bits;
    uint8_t cursor;
    uint16_t score;
    bool mismatch;
} BitLab;

static void bit_lab_draw(Canvas* canvas, void* context) {
    BitLab* state = context;
    furi_mutex_acquire(state->mutex, FuriWaitForever);
    canvas_clear(canvas);
    canvas_set_font(canvas, FontSecondary);
    char line[32];
    snprintf(line, sizeof(line), "Match %02X   Score %u", state->target, (unsigned)state->score);
    canvas_draw_str(canvas, 2, 10, line);
    for(uint8_t i = 0; i < 8; i++) {
        uint8_t x = 3 + 15 * i;
        canvas_draw_frame(canvas, x, 19, 13, 18);
        char bit[2] = {(state->bits & (1U << (7 - i))) ? '1' : '0', '\0'};
        canvas_draw_str(canvas, x + 4, 32, bit);
        if(i == state->cursor) canvas_draw_line(canvas, x, 40, x + 12, 40);
    }
    canvas_draw_str(canvas, 2, 51, state->mismatch ? "Try again" : "L/R move  U/D flip");
    canvas_draw_str(canvas, 2, 62, "OK check  Back exit");
    furi_mutex_release(state->mutex);
}

static void bit_lab_input(InputEvent* event, void* context) {
    /* Do not block the input callback if the queue is full. */
    furi_message_queue_put(context, event, 0);
}

int32_t bit_lab_app(void* argument) {
    UNUSED(argument);
    BitLab state = {.target = 0x5A, .bits = 0, .cursor = 0, .score = 0, .mismatch = false};
    state.mutex = furi_mutex_alloc(FuriMutexTypeNormal);
    FuriMessageQueue* queue = furi_message_queue_alloc(8, sizeof(InputEvent));
    ViewPort* viewport = view_port_alloc();
    view_port_draw_callback_set(viewport, bit_lab_draw, &state);
    view_port_input_callback_set(viewport, bit_lab_input, queue);
    Gui* gui = furi_record_open(RECORD_GUI);
    gui_add_view_port(gui, viewport, GuiLayerFullscreen);
    bool running = true;
    while(running) {
        InputEvent event;
        if(furi_message_queue_get(queue, &event, 100) != FuriStatusOk) continue;
        if(event.type != InputTypeShort && event.type != InputTypeRepeat) continue;
        furi_mutex_acquire(state.mutex, FuriWaitForever);
        switch(event.key) {
        case InputKeyBack: running = false; break;
        case InputKeyLeft: state.cursor = (state.cursor + 7) % 8; break;
        case InputKeyRight: state.cursor = (state.cursor + 1) % 8; break;
        case InputKeyUp:
        case InputKeyDown:
            state.bits ^= 1U << (7 - state.cursor);
            state.mismatch = false;
            break;
        case InputKeyOk:
            if(state.bits == state.target) {
                state.score++;
                /* Deterministic exercise targets, not security randomness. */
                state.target = (uint8_t)(state.target * 73U + 41U);
                state.bits = 0;
                state.mismatch = false;
            } else {
                state.mismatch = true;
            }
            break;
        default: break;
        }
        furi_mutex_release(state.mutex);
        view_port_update(viewport);
    }
    view_port_enabled_set(viewport, false);
    gui_remove_view_port(gui, viewport);
    view_port_free(viewport);
    furi_message_queue_free(queue);
    furi_mutex_free(state.mutex);
    furi_record_close(RECORD_GUI);
    return 0;
}
