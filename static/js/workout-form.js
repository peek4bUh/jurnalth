const workoutForm = document.getElementById("workout-form");
const formsContainer = document.getElementById("exercise-forms");
const totalForms = document.getElementById("id_exercises-TOTAL_FORMS");
const addExerciseButton = document.getElementById("add-exercise");
const emptyForm = document.getElementById("empty-exercise-form").innerHTML;
const lastExerciseDataUrl = workoutForm.dataset.lastExerciseDataUrl;
const workoutStateKey = "jurnalth-workout-form";

async function fillLastExerciseData(select) {
    const row = select.closest(".exercise-row");
    const volumeInput = row.querySelector("input[name$='-volume']");
    const restInput = row.querySelector("input[name$='-rest']");
    const lastVolumeElements = row.querySelectorAll(".last-volume");
    if (!select.value || !volumeInput) {
        lastVolumeElements.forEach((element) => {
            element.textContent = "";
        });
        return;
    }
    lastVolumeElements.forEach((element) => {
        element.textContent = "No volume data";
    });

    try {
        const response = await fetch(
            lastExerciseDataUrl.replace("/0/", `/${select.value}/`));
        if (!response.ok) {
            lastVolumeElements.forEach((element) => {
                element.textContent = "No volume data";
            });
            return;
        }

        const data = await response.json();
        volumeInput.value = data.volume;
        if (restInput) restInput.value = data.rest;
        lastVolumeElements.forEach((element) => {
            element.textContent = data.volume ? `${data.volume}` : "No volume data";
        });
        updateExerciseSummary(select.closest(".exercise-row"));
    } catch (error) {
        lastVolumeElements.forEach((element) => {
            element.textContent = "No volume data";
        });
    }
}

function updateExerciseSummary(row) {
    if (!row) return;
    const exerciseField = row.querySelector("[name$='-exercise']");
    const nameElement = row.querySelector(".exercise-summary-name");
    if (!nameElement) return;

    const fieldName = exerciseField?.dataset?.name?.trim();
    if (fieldName) {
        nameElement.textContent = fieldName;
        nameElement.dataset.exerciseName = fieldName;
        return;
    }

    if (exerciseField?.value && nameElement.textContent.trim() === "Choose an exercise") {
        nameElement.textContent = "Exercise selected";
        nameElement.dataset.exerciseName = "";
    }
}

function syncVolumeFromSets(row) {
    const volumeInput = row.querySelector("input[name$='-volume']");
    if (!volumeInput) return;

    const sets = [...row.querySelectorAll(".set-row")].map((set) => {
        const weight = set.querySelector(".set-weight").value.trim();
        const reps = set.querySelector(".set-reps").value.trim();
        if (!weight && !reps) return "";
        return `1x${weight || ""}x${reps || ""}`;
    }).filter(Boolean);
    if (sets.length) volumeInput.value = sets.join(", ");
    updateExerciseSummary(row);
}

function renumberSets(row) {
    row.querySelectorAll(".set-row").forEach((set, index) => {
        set.querySelector(".set-number").textContent = index + 1;
    });
}

function renumberForms() {
    const rows = formsContainer.querySelectorAll(".exercise-row");
    rows.forEach((row, index) => {
        row.querySelectorAll("[name], [id], [for]").forEach((element) => {
            ["name", "id", "for"].forEach((attribute) => {
                const value = element.getAttribute(attribute);
                if (value) element.setAttribute(attribute, value.replace(/exercises-(?:\d+|__prefix__)-/, `exercises-${index}-`));
            });
        });

        row.querySelector(".move-exercise-up").disabled = index === 0;
        row.querySelector(".move-exercise-down").disabled = index === rows.length - 1;
    });
    totalForms.value = rows.length;
}

function addSelectedExercise() {
    const params = new URLSearchParams(window.location.search);
    const urlExerciseIds = params.getAll("exercise_id");
    const urlExerciseNames = params.getAll("exercise_name");

    let savedSelection = [];
    try {
        savedSelection = JSON.parse(localStorage.getItem("jurnalth-selected-exercises") || "[]");
    } catch (error) {
        localStorage.removeItem("jurnalth-selected-exercises");
    }

    const selection = urlExerciseIds.length
        ? urlExerciseIds.map((id, index) => ({ id, name: urlExerciseNames[index] || "" }))
        : savedSelection;

    const existingIds = [...formsContainer.querySelectorAll("[name$='-exercise']")]
        .map((field) => String(field.value))
        .filter(Boolean);

    const validSelection = selection.filter((item) => item && item.id && !existingIds.includes(String(item.id)));
    if (!validSelection.length) return;

    validSelection.forEach(({ id, name }) => {
        const row = addEmptyRow();

        const exerciseField = row.querySelector("[name$='-exercise']");
        exerciseField.value = id;
        exerciseField.dataset.name = name || "";

        if (name) {
            row.querySelector(".exercise-summary-name").textContent = name;
        }

        updateExerciseSummary(row);
        fillLastExerciseData(exerciseField);
    });

    window.history.replaceState({}, document.title, window.location.pathname);
}

function addEmptyRow() {
    formsContainer.insertAdjacentHTML("beforeend", emptyForm.replaceAll("__prefix__", formsContainer.children.length));
    renumberForms();
    return formsContainer.lastElementChild;
}

function saveWorkoutState() {
    const fields = [...workoutForm.elements]
        .filter((element) => element.name && element.type !== "submit")
        .map((element) => ({
            name: element.name,
            value: element.value,
            checked: element.checked,
        }));
    const names = [...formsContainer.querySelectorAll(".exercise-summary-name")]
        .map((element) => element.textContent.trim());
    localStorage.setItem(workoutStateKey, JSON.stringify({ fields, names }));
}

function restoreWorkoutState() {
    const savedFields = localStorage.getItem(workoutStateKey);
    if (!savedFields) return;

    const savedState = JSON.parse(savedFields);
    const fieldsToRestore = savedState.fields || savedState;
    const rowIndexes = fieldsToRestore
        .map((field) => field.name.match(/^exercises-(\d+)-/))
        .filter(Boolean)
        .map((match) => Number(match[1]));
    const rowsNeeded = rowIndexes.length ? Math.max(...rowIndexes) + 1 : 0;
    while (formsContainer.children.length < rowsNeeded) addEmptyRow();

    fieldsToRestore.forEach((savedField) => {
        const fields = [...workoutForm.elements].filter(
            (element) => element.name === savedField.name);
        const field = fields[0];
        if (!field) return;
        field.value = savedField.value;
        if (field.type === "checkbox") field.checked = savedField.checked;
    });
    (savedState.names || []).forEach((name, index) => {
        const nameElement = formsContainer.children[index]?.querySelector(".exercise-summary-name");
        if (nameElement && name) nameElement.textContent = name;
    });
    localStorage.removeItem(workoutStateKey);
}

addExerciseButton.addEventListener("click", (event) => {
    event.preventDefault();
    saveWorkoutState();
    window.location.href = addExerciseButton.href;
});

formsContainer.addEventListener("click", (event) => {
    const row = event.target.closest(".exercise-row");
    if (!row) return;

    if (event.target.classList.contains("remove-exercise")) {
        const deleteInput = row.querySelector("input[name$='-DELETE']");
        if (deleteInput) {
            deleteInput.checked = true;
            row.classList.add("hidden");
        } else {
            row.remove();
        }
        renumberForms();
    }

    if (event.target.classList.contains("toggle-exercise-edit")) {
        const fields = row.querySelector(".exercise-edit-fields");
        const isCollapsed = fields.classList.toggle("hidden");
        event.target.textContent = isCollapsed ? "Edit" : "Close";
        event.target.setAttribute("aria-expanded", String(!isCollapsed));
    }

    if (event.target.classList.contains("add-set")) {
        const rows = row.querySelector(".set-rows");
        rows.insertAdjacentHTML("beforeend", `
            <div class="set-row flex items-center py-2 transition-colors hover:bg-gray-50">
                <p class="set-number w-12 shrink-0 text-sm text-gray-500"></p>
                <p class="min-w-0 grow basis-0"><input type="number" min="1" class="set-reps w-full min-w-0 rounded-sm border border-gray-200 px-2 py-1.5 text-sm focus:border-gray-700 focus:outline-none focus:ring-0"></p>
                <p class="min-w-0 grow basis-0 px-2"><input type="number" step="0.5" class="set-weight w-full min-w-0 rounded-sm border border-gray-200 px-2 py-1.5 text-sm focus:border-gray-700 focus:outline-none focus:ring-0"></p>
                <p class="flex w-8 shrink-0 justify-center"><button type="button" class="remove-set inline-flex h-7 w-7 cursor-pointer items-center justify-center rounded-sm text-sm font-medium text-gray-400 transition-colors hover:bg-gray-200 hover:text-gray-900" title="Delete set" aria-label="Delete set">×</button></p>
            </div>`);
        renumberSets(row);
    }

    if (event.target.classList.contains("remove-set")) {
        event.target.closest(".set-row").remove();
        renumberSets(row);
        syncVolumeFromSets(row);
    }

    if (event.target.classList.contains("move-exercise-up")) {
        const previousRow = row.previousElementSibling;
        if (previousRow) formsContainer.insertBefore(row, previousRow);
        renumberForms();
    }

    if (event.target.classList.contains("move-exercise-down")) {
        const nextRow = row.nextElementSibling;
        if (nextRow) formsContainer.insertBefore(nextRow, row);
        renumberForms();
    }
});

formsContainer.addEventListener("change", (event) => {
    if (event.target.matches("[name$='-exercise']")) {
        updateExerciseSummary(event.target.closest(".exercise-row"));
        fillLastExerciseData(event.target);
    }
});

formsContainer.addEventListener("input", (event) => {
    if (event.target.matches(".set-weight, .set-reps")) {
        syncVolumeFromSets(event.target.closest(".exercise-row"));
    }
    if (event.target.matches("input[name$='-volume'], input[name$='-rest']")) {
        updateExerciseSummary(event.target.closest(".exercise-row"));
    }
});

workoutForm.addEventListener("submit", () => {
    formsContainer.querySelectorAll(".exercise-row").forEach(syncVolumeFromSets);
    localStorage.removeItem("jurnalth-selected-exercises");
});

restoreWorkoutState();
renumberForms();
addSelectedExercise();
