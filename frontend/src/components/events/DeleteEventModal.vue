<script setup>
import { useEventsStore } from "@/stores";
import { storeToRefs } from "pinia";

const eventsStore = useEventsStore();
const { status } = storeToRefs(eventsStore);

const props = defineProps(["event_id", "modal"]);
const emit = defineEmits(["event-deleted"]);

function onSubmit() {
  return eventsStore
    .delete(props.event_id)
    .then(() => {
      emit("event-deleted", { event_id: props.event_id });
      props.modal.hide();
    })
    .catch((error) => (status.error = error));
}
</script>

<template>
  <div
    :id="'deleteEventModal_' + event_id"
    class="modal fade"
    tabindex="-1"
    aria-labelledby="deleteEventModal"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="deleteEventModal">
            Delete Event #{{ event_id }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Discard"
          ></button>
        </div>
        <div class="modal-body">
          Are you sure you want to delete this event?
        </div>
        <div v-if="status.error" class="w-100 alert alert-danger mt-3 mb-3">
          {{ status.error }}
        </div>
        <div class="modal-footer">
          <button
            id="closeModalButton"
            type="button"
            data-bs-dismiss="modal"
            class="btn btn-secondary"
          >
            Discard
          </button>
          <button
            type="submit"
            @click="onSubmit"
            class="btn btn-danger"
            :class="{ disabled: status.deleting }"
          >
            <span v-if="status.deleting">
              <span
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              ></span>
            </span>
            <span v-if="!status.deleting">Delete</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
