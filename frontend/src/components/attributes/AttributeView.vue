<script setup>
import SightingsSparklineWidget from "@/components/sightings/SightingsSparklineWidget.vue";
import SightingsStatsWidget from "@/components/sightings/SightingsStatsWidget.vue";
import TagsIndex from "@/components/tags/TagsIndex.vue";
import DistributionLevel from "@/components/enums/DistributionLevel.vue";
import DeleteAttributeModal from "@/components/attributes/DeleteAttributeModal.vue";

defineProps(["attribute", "status"]);

function handleAttributeDeleted() {
  router.go(-1);
}
</script>

<style>
.single-stat-card .card-body {
  font-size: x-large;
  text-align: center;
  padding: 0;
}

div.row h3 {
  margin-bottom: 0;
}

.single-stat-card .card-body p {
  margin-bottom: 0;
}
</style>
<template>
  <div class="card">
    <div class="attribute-title card-header border-bottom">
      <div class="row">
        <div class="col-10">
          <h3>Attribute #{{ attribute.id }}</h3>
        </div>
        <div class="col-2 text-end">
          <div
            class="flex-wrap"
            :class="{
              'btn-group-vertical': $isMobile,
              'btn-group': !$isMobile,
            }"
            aria-label="Attribute Actions"
          >
            <button
              type="button"
              class="btn btn-danger"
              data-bs-toggle="modal"
              :data-bs-target="'#deleteAttributeModal-' + attribute.id"
            >
              <font-awesome-icon icon="fa-solid fa-trash" />
            </button>
            <RouterLink
              :to="`/attributes/update/${attribute.id}`"
              class="btn btn-outline-primary"
            >
              <font-awesome-icon icon="fa-solid fa-pen" />
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
    <div class="row m-1">
      <div class="col-sm-6 mt-2">
        <div class="card">
          <div class="card-body d-flex flex-column">
            <div class="table-responsive-sm">
              <table class="table table-striped">
                <tbody>
                  <tr>
                    <th>id</th>
                    <td>{{ attribute.id }}</td>
                  </tr>
                  <tr>
                    <th>uuid</th>
                    <td>
                      {{ attribute.uuid }}
                      <font-awesome-icon
                        class="text-primary"
                        icon="fa-solid fa-copy"
                      />
                    </td>
                  </tr>
                  <tr>
                    <th>event_id</th>
                    <td>{{ attribute.event_id }}</td>
                  </tr>
                  <tr>
                    <th>category</th>
                    <td>{{ attribute.category }}</td>
                  </tr>
                  <tr>
                    <th>type</th>
                    <td>{{ attribute.type }}</td>
                  </tr>
                  <tr>
                    <th>value</th>
                    <td>{{ attribute.value }}</td>
                  </tr>
                  <tr>
                    <th>comment</th>
                    <td>{{ attribute.comment }}</td>
                  </tr>
                  <tr>
                    <th>timestamp</th>
                    <td>{{ attribute.timestamp }}</td>
                  </tr>
                  <tr>
                    <th>distribution</th>
                    <td>
                      <DistributionLevel
                        :distribution_level_id="attribute.distribution"
                      />
                    </td>
                  </tr>
                  <tr>
                    <th>disable correlation</th>
                    <td>
                      <div class="form-check form-switch">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          :checked="attribute.disable_correlation"
                          disabled
                        />
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <th>to IDS</th>
                    <td>
                      <div class="form-check form-switch">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          :checked="attribute.to_ids"
                          disabled
                        />
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <th>first seen</th>
                    <td>{{ attribute.first_seen }}</td>
                  </tr>
                  <tr>
                    <th>last seen</th>
                    <td>{{ attribute.last_seen }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-12 col-sm-12 col-md-12 col-lg-6 col-xl-3">
        <SightingsSparklineWidget :value="attribute.value" />
        <SightingsStatsWidget :value="attribute.value" />
      </div>
      <div class="col col-sm-6">
        <div class="card mt-2">
          <div class="card-header">
            <font-awesome-icon icon="fa-solid fa-tags" /> tags
          </div>
          <div class="card-body d-flex flex-column">
            <div class="card-text">
              <TagsIndex :tags="attribute.tags" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <DeleteAttributeModal
      @attribute-deleted="handleAttributeDeleted"
      :attribute_id="attribute.id"
    />
  </div>
</template>
