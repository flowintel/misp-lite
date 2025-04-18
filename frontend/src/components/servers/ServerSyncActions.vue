<script setup>
import { useServersStore } from "@/stores";
import {
  faCheck,
  faDownload,
  faMagnifyingGlass,
  faSync,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
const serversStore = useServersStore();

defineProps(["server"]);

function testServerConnection(server) {
  server.testingConnection = true;
  serversStore
    .testConnection(server.id)
    .then((response) => {
      if (response.status == "ok") {
        server.connectionSucceeded = true;
      } else {
        server.connectionSucceeded = false;
        server.connectionFailed = true;
        server.connectionError = response.error;
      }
      server.testingConnection = false;
    })
    .catch((error) => {
      server.connectionSucceeded = false;
      setErrors({ apiError: error });
    })
    .finally(() => {
      server.testingConnection = false;
    });
}

function pullServer(server) {
  serversStore.pull(server.id);
}
</script>

<template>
  <div class="flex-wrap btn-group" aria-label="Sync Actions">
    <button
      v-if="
        !server.testingConnection &&
        !server.connectionSucceeded &&
        !server.connectionFailed
      "
      type="button"
      class="btn btn-outline-primary"
      @click="testServerConnection(server)"
      data-toggle="tooltip"
      data-placement="top"
      title="Check connection"
    >
      <FontAwesomeIcon :icon="faCheck" />
    </button>
    <button v-if="server.testingConnection" type="button" class="btn btn-light">
      <FontAwesomeIcon :icon="faSync" spin />
    </button>
    <button
      v-if="
        !server.testingConnection &&
        server.connectionFailed &&
        !server.connectionSucceeded
      "
      type="button"
      class="btn btn-danger"
      @click="testServerConnection(server)"
      data-toggle="tooltip"
      data-placement="top"
      :title="'Connection failed: ' + server.connectionError"
    >
      <FontAwesomeIcon :icon="faXmark" />
    </button>
    <button
      v-if="server.connectionSucceeded"
      type="button"
      class="btn btn-success"
      data-toggle="tooltip"
      data-placement="top"
      title="Connection succeed"
    >
      <FontAwesomeIcon :icon="faCheck" />
    </button>
    <!-- <button type="button" class="btn btn-outline-primary" disabled data-toggle="tooltip" data-placement="top"
            title="Push">
            <FontAwesomeIcon :icon="faUpload" />
        </button> -->
    <button
      type="button"
      class="btn btn-outline-primary"
      data-placement="top"
      title="Pull"
      @click="pullServer(server)"
    >
      <FontAwesomeIcon :icon="faDownload" />
    </button>
    <RouterLink
      :to="`/servers/explore/${server.id}`"
      class="btn btn-outline-primary"
    >
      <FontAwesomeIcon :icon="faMagnifyingGlass" />
    </RouterLink>
  </div>
</template>
