const API_BASE = ""; // Nginx проксирует /events на FastAPI.

const elements = {
  apiStatus: document.querySelector("#apiStatus"),
  apiStatusText: document.querySelector("#apiStatusText"),
  totalEvents: document.querySelector("#totalEvents"),
  totalRegistrations: document.querySelector("#totalRegistrations"),
  totalAvailable: document.querySelector("#totalAvailable"),
  eventCount: document.querySelector("#eventCount"),
  eventsList: document.querySelector("#eventsList"),
  createForm: document.querySelector("#createEventForm"),
  refreshButton: document.querySelector("#refreshButton"),
  searchInput: document.querySelector("#searchInput"),
  sortSelect: document.querySelector("#sortSelect"),
  registrationDialog: document.querySelector("#registrationDialog"),
  registrationForm: document.querySelector("#registrationForm"),
  registrationEventName: document.querySelector("#registrationEventName"),
  closeRegistration: document.querySelector("#closeRegistration"),
  toastRegion: document.querySelector("#toastRegion"),
};

let eventsWithStats = [];

async function apiRequest(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (options.body) headers["Content-Type"] = "application/json";
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (response.status === 204) return null;

  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const detail = typeof payload === "object" && payload !== null
      ? (payload.detail || "Не удалось выполнить запрос")
      : (payload || "Не удалось выполнить запрос");
    throw new Error(Array.isArray(detail) ? detail.map(item => item.msg || JSON.stringify(item)).join("; ") : String(detail));
  }
  return payload;
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, character => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[character]);
}

function displayDate(value) {
  if (!value) return { day: "—", month: "—", full: "Дата не указана" };
  // FastAPI возвращает datetime без часового пояса; браузер трактует его как локальное время.
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return { day: "—", month: "—", full: String(value) };
  return {
    day: new Intl.DateTimeFormat("ru-RU", { day: "2-digit" }).format(date),
    month: new Intl.DateTimeFormat("ru-RU", { month: "short" }).format(date).replace(".", ""),
    full: new Intl.DateTimeFormat("ru-RU", { dateStyle: "medium", timeStyle: "short" }).format(date),
    sort: date.getTime(),
  };
}

function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;
  elements.toastRegion.appendChild(toast);
  window.setTimeout(() => toast.remove(), 4200);
}

function updateApiStatus(online, message = "") {
  elements.apiStatus.classList.toggle("online", online);
  elements.apiStatus.classList.toggle("offline", !online);
  elements.apiStatusText.textContent = online ? "API онлайн" : (message || "API недоступен");
}

function renderLoading() {
  elements.eventsList.innerHTML = '<div class="loading-state"><span class="spinner"></span><span>Загружаем мероприятия…</span></div>';
}

function renderError(message) {
  elements.eventsList.innerHTML = `<div class="error-state"><strong>Не удалось загрузить мероприятия</strong><br>${escapeHtml(message)}<br><button class="button button-quiet" id="retryLoad" type="button" style="margin-top:14px">Повторить</button></div>`;
  document.querySelector("#retryLoad")?.addEventListener("click", loadEvents);
}

function sortedFilteredEvents() {
  const query = elements.searchInput.value.trim().toLocaleLowerCase("ru-RU");
  const sort = elements.sortSelect.value;
  const list = eventsWithStats.filter(({ event }) =>
    `${event.title} ${event.location} ${event.description || ""}`.toLocaleLowerCase("ru-RU").includes(query)
  );
  return list.sort((a, b) => {
    if (sort === "title") return a.event.title.localeCompare(b.event.title, "ru");
    if (sort === "available") return a.stats.available_places - b.stats.available_places;
    return (displayDate(a.event.starts_at).sort || 0) - (displayDate(b.event.starts_at).sort || 0);
  });
}

function eventCard({ event, stats }) {
  const date = displayDate(event.starts_at);
  const capacity = Number(stats.capacity || event.capacity || 0);
  const registered = Number(stats.registered_count || 0);
  const available = Number(stats.available_places ?? Math.max(0, capacity - registered));
  const percent = capacity > 0 ? Math.min(100, Math.round((registered / capacity) * 100)) : 0;
  const full = available <= 0;
  return `
    <article class="event-card">
      <div class="date-tile"><span class="date-month">${escapeHtml(date.month)}</span><span class="date-day">${escapeHtml(date.day)}</span></div>
      <div class="event-main">
        <div class="event-head">
          <div><h3 class="event-title">${escapeHtml(event.title)}</h3><div class="event-id">EVENT #${escapeHtml(event.id)}</div></div>
          <button class="icon-button delete-event" type="button" data-id="${escapeHtml(event.id)}" aria-label="Удалить мероприятие ${escapeHtml(event.title)}" title="Удалить мероприятие">×</button>
        </div>
        <div class="event-meta"><span><span aria-hidden="true">◷</span>${escapeHtml(date.full)}</span><span><span aria-hidden="true">⌖</span>${escapeHtml(event.location)}</span></div>
        ${event.description ? `<p class="event-description">${escapeHtml(event.description)}</p>` : ""}
        <div class="event-bottom">
          <div class="capacity-block">
            <div class="capacity-copy"><strong>${registered}</strong> из ${capacity} мест занято · <strong>${available}</strong> свободно</div>
            <div class="capacity-track"><div class="capacity-fill ${full ? "full" : ""}" style="width:${percent}%"></div></div>
          </div>
          <div class="card-actions"><button class="button small-button register-event" type="button" data-id="${escapeHtml(event.id)}" data-title="${escapeHtml(event.title)}" ${full ? "disabled" : ""}>${full ? "Мест нет" : "Записать участника"}</button></div>
        </div>
      </div>
    </article>`;
}

function renderEvents() {
  const events = sortedFilteredEvents();
  elements.eventCount.textContent = String(eventsWithStats.length);
  if (!events.length) {
    elements.eventsList.innerHTML = `<div class="empty-state"><div class="empty-icon">✳</div><strong>${eventsWithStats.length ? "Ничего не найдено" : "Пока нет мероприятий"}</strong><br>${eventsWithStats.length ? "Попробуй изменить поисковый запрос." : "Создай первое мероприятие в форме справа — оно появится здесь."}</div>`;
    return;
  }
  elements.eventsList.innerHTML = events.map(eventCard).join("");
  elements.eventsList.querySelectorAll(".register-event").forEach(button => {
    button.addEventListener("click", () => openRegistration(button.dataset.id, button.dataset.title));
  });
  elements.eventsList.querySelectorAll(".delete-event").forEach(button => {
    button.addEventListener("click", () => removeEvent(button.dataset.id));
  });
}

async function loadEvents() {
  renderLoading();
  elements.refreshButton.disabled = true;
  try {
    const events = await apiRequest("/events");
    const rows = await Promise.all(events.map(async event => {
      try {
        const stats = await apiRequest(`/events/${event.id}/registrations/stats`);
        return { event, stats };
      } catch (error) {
        return { event, stats: { event_id: event.id, registered_count: 0, capacity: event.capacity, available_places: event.capacity }, statsError: error.message };
      }
    }));
    eventsWithStats = rows;
    updateApiStatus(true);
    elements.totalEvents.textContent = String(rows.length);
    elements.totalRegistrations.textContent = String(rows.reduce((sum, row) => sum + Number(row.stats.registered_count || 0), 0));
    elements.totalAvailable.textContent = String(rows.reduce((sum, row) => sum + Number(row.stats.available_places ?? 0), 0));
    renderEvents();
  } catch (error) {
    updateApiStatus(false);
    renderError(error.message);
    elements.totalEvents.textContent = "—";
    elements.totalRegistrations.textContent = "—";
    elements.totalAvailable.textContent = "—";
  } finally {
    elements.refreshButton.disabled = false;
  }
}

elements.createForm.addEventListener("submit", async event => {
  event.preventDefault();
  const form = event.currentTarget;
  const submit = form.querySelector("button[type=submit]");
  const formData = new FormData(form);
  const startsAt = String(formData.get("starts_at") || "");
  const payload = {
    title: String(formData.get("title") || "").trim(),
    location: String(formData.get("location") || "").trim(),
    starts_at: startsAt.length === 16 ? `${startsAt}:00` : startsAt,
    capacity: Number(formData.get("capacity")),
    description: String(formData.get("description") || "").trim() || null,
  };
  submit.disabled = true;
  submit.querySelector("span").textContent = "Создаём…";
  try {
    await apiRequest("/events", { method: "POST", body: JSON.stringify(payload) });
    form.reset();
    form.elements.capacity.value = "30";
    showToast("Мероприятие создано");
    await loadEvents();
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    submit.disabled = false;
    submit.querySelector("span").textContent = "Создать мероприятие";
  }
});

function openRegistration(eventId, title) {
  elements.registrationForm.reset();
  elements.registrationForm.elements.event_id.value = eventId;
  elements.registrationEventName.textContent = title;
  elements.registrationDialog.showModal();
}

elements.closeRegistration.addEventListener("click", () => elements.registrationDialog.close());
elements.registrationDialog.addEventListener("click", event => {
  if (event.target === elements.registrationDialog) elements.registrationDialog.close();
});

elements.registrationForm.addEventListener("submit", async event => {
  event.preventDefault();
  const form = event.currentTarget;
  const submit = form.querySelector("button[type=submit]");
  submit.disabled = true;
  submit.querySelector("span").textContent = "Регистрируем…";
  try {
    const eventId = form.elements.event_id.value;
    await apiRequest(`/events/${eventId}/registrations`, {
      method: "POST",
      body: JSON.stringify({
        attendee_name: form.elements.attendee_name.value.trim(),
        attendee_email: form.elements.attendee_email.value.trim(),
      }),
    });
    elements.registrationDialog.close();
    showToast("Участник зарегистрирован");
    await loadEvents();
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    submit.disabled = false;
    submit.querySelector("span").textContent = "Подтвердить регистрацию";
  }
});

async function removeEvent(id) {
  const item = eventsWithStats.find(row => String(row.event.id) === String(id));
  if (!item) return;
  if (!window.confirm(`Удалить мероприятие «${item.event.title}» и его регистрации?`)) return;
  try {
    await apiRequest(`/events/${id}`, { method: "DELETE" });
    showToast("Мероприятие удалено");
    await loadEvents();
  } catch (error) {
    showToast(error.message, "error");
  }
}

elements.refreshButton.addEventListener("click", loadEvents);
elements.searchInput.addEventListener("input", renderEvents);
elements.sortSelect.addEventListener("change", renderEvents);
loadEvents();
