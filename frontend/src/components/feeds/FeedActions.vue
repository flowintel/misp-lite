<script setup>
import { ref, onMounted } from "vue";
import { Modal } from "bootstrap";
import { useFeedsStore } from "@/stores";
import { useToastsStore } from "@/stores";
import DeleteFeedModal from "@/components/feeds/DeleteFeedModal.vue";

const props = defineProps(["feed"]);
const emit = defineEmits(["feed-deleted"]);

const deleteFeedModal = ref(null);
const feedsStore = useFeedsStore();
const toastsStore = useToastsStore();

onMounted(() => {
  deleteFeedModal.value = new Modal(
    document.getElementById(`deleteFeedModal_${props.feed.id}`),
  );
});

function openDeleteFeedModal() {
  deleteFeedModal.value.show();
}

function handleFeedDeleted() {
  emit("feed-deleted", props.feed.id);
}

function fetchFeed(feed) {
  feedsStore
    .fetch(feed.id)
    .then((response) => {
      toastsStore.push("Feed fetch enqueued. Task ID: " + response.task.id);
    })
    .catch((error) => {
      toastsStore.push("Error fetching feed: " + error, "error");
    });
}
</script>

<style scoped>
.btn-toolbar {
  flex-wrap: nowrap !important;
}
</style>

<template>
  <div>
    <div class="btn-toolbar float-end" role="toolbar">
      <div class="flex-wrap btn-group me-2" aria-label="Sync Actions">
        <button
          type="button"
          class="btn btn-outline-primary"
          data-placement="top"
          title="Fetch"
          @click="fetchFeed(feed)"
          :class="{ disabled: !feed.enabled }"
        >
          <font-awesome-icon icon="fa-solid fa-download" />
        </button>
        <button
          type="button"
          class="btn btn-outline-primary"
          data-toggle="tooltip"
          data-placement="top"
          title="Preview"
          disabled
        >
          <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
        </button>
      </div>
      <div
        :class="{
          'btn-group-vertical': $isMobile,
          'btn-group me-2': !$isMobile,
        }"
        role="group"
        aria-label="Feed Actions"
      >
        <RouterLink :to="`/feeds/${feed.id}`" class="btn btn-outline-primary">
          <font-awesome-icon icon="fa-solid fa-eye" />
        </RouterLink>
        <RouterLink
          :to="`/feeds/update/${feed.id}`"
          class="btn btn-outline-primary"
        >
          <font-awesome-icon icon="fa-solid fa-pen" />
        </RouterLink>
      </div>
      <div class="btn-group me-2" role="group">
        <button
          type="button"
          class="btn btn-danger"
          @click="openDeleteFeedModal"
        >
          <font-awesome-icon icon="fa-solid fa-trash" />
        </button>
      </div>
    </div>
    <DeleteFeedModal
      :key="feed.id"
      :id="`deleteFeedModal_${feed.id}`"
      @feed-deleted="handleFeedDeleted"
      :modal="deleteFeedModal"
      :feed_id="feed.id"
    />
  </div>
</template>
