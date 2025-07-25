<script setup>
import { ref } from "vue";
import { useAttributesStore } from "@/stores";
import { errorHandler } from "@/helpers";
import { storeToRefs } from "pinia";
import { AttributeSchema } from "@/schemas/attribute";
import { DISTRIBUTION_LEVEL } from "@/helpers/constants";
import DistributionLevelSelect from "@/components/enums/DistributionLevelSelect.vue";
import ApiError from "@/components/misc/ApiError.vue";
import AttributeCategorySelect from "@/components/enums/AttributeCategorySelect.vue";
import AttributeTypeSelect from "@/components/enums/AttributeTypeSelect.vue";
import Datepicker from "@/components/misc/Datepicker.vue";
import { Form, Field } from "vee-validate";

const attributesStore = useAttributesStore();
const { status } = storeToRefs(attributesStore);
const apiError = ref(null);
const props = defineProps(["event_uuid", "modal"]);
const emit = defineEmits(["attribute-created"]);

const attribute = ref({
  distribution: DISTRIBUTION_LEVEL.INHERIT_EVENT,
  event_uuid: props.event_uuid,
  category: "Network activity",
  type: "ip-src",
  disable_correlation: false,
});

function addAttribute(values, { setErrors }) {
  apiError.value = null;
  return attributesStore
    .create(attribute.value)
    .then((response) => {
      emit("attribute-created", { attribute: response });
      props.modal.hide();
    })
    .catch((errors) => {
      apiError.value = errors;
      setErrors(errorHandler.transformApiToFormErrors(errors));
    });
}

function onClose() {
  attribute.value = {
    distribution: DISTRIBUTION_LEVEL.INHERIT_EVENT,
    event_uuid: props.event_uuid,
    category: "Network activity",
    type: "ip-src",
    disable_correlation: false,
  };
}

function handleAttributeCategoryUpdated(category) {
  attribute.value.category = category;
}

function handleAttributeTypeUpdated(type) {
  attribute.value.type = type;
}

function handleDistributionLevelUpdated(distributionLevelId) {
  attribute.value.distribution = parseInt(distributionLevelId);
}
</script>

<template>
  <div
    id="addAttributeModal"
    class="modal"
    aria-labelledby="addAttributeModal"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <Form
        @submit="addAttribute"
        :validation-schema="AttributeSchema"
        v-slot="{ errors }"
      >
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addAttributeModalLabel">
              Add Attribute
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Discard"
            ></button>
          </div>
          <div class="modal-body">
            <div class="row m-2">
              <div class="col text-start">
                <label for="attribute.category" class="form-label"
                  >category</label
                >
                <AttributeCategorySelect
                  name="attribute.category"
                  :selected="attribute.category"
                  @attribute-category-updated="handleAttributeCategoryUpdated"
                  :errors="errors['attribute.category']"
                />
                <div class="invalid-feedback">
                  {{ errors["attribute.category"] }}
                </div>
              </div>
              <div class="col text-start">
                <label for="attribute.type" class="form-label">type</label>
                <AttributeTypeSelect
                  :key="attribute.category"
                  name="attribute.type"
                  :category="attribute.category"
                  :selected="attribute.type"
                  @attribute-type-updated="handleAttributeTypeUpdated"
                  :errors="errors['attribute.type']"
                />
                <div class="invalid-feedback">
                  {{ errors["attribute.type"] }}
                </div>
              </div>
            </div>
            <div class="row m-2">
              <div class="col col-6 text-start">
                <label for="attribute.distribution" class="form-label"
                  >distribution</label
                >
                <DistributionLevelSelect
                  name="attribute.distribution"
                  :selected="attribute.distribution"
                  @distribution-level-updated="handleDistributionLevelUpdated"
                  :errors="errors['attribute.distribution']"
                />
                <div class="invalid-feedback">
                  {{ errors["attribute.distribution"] }}
                </div>
              </div>
            </div>
            <!-- TODO: sharing groups -->
            <!-- <div class="row m-2"> -->
            <!-- <div class="col col-6 text-start">
                  <label for="attributeSharingGroupId" class="form-label">Sharing Group</label>
                  <SharingGroupSelect v-model=attribute.sharing_group_id />
                  <div class="invalid-feedback">{{ errors[attribute.sharing_group_id'] }}</div>
                </div>
              </div> -->
            <div class="row m-2">
              <div class="col text-start">
                <label for="attribute.value">value</label>
                <Field
                  class="form-control"
                  id="attribute.value"
                  name="attribute.value"
                  as="textarea"
                  v-model="attribute.value"
                  style="height: 100px"
                  :class="{ 'is-invalid': errors['attribute.value'] }"
                >
                </Field>
                <div class="invalid-feedback">
                  {{ errors["attribute.value"] }}
                </div>
              </div>
            </div>
            <div class="row m-2">
              <div class="col text-start">
                <label for="attribute.comment">comment</label>
                <Field
                  class="form-control"
                  id="attribute.comment"
                  name="attribute.comment"
                  as="textarea"
                  v-model="attribute.comment"
                  style="height: 100px"
                  :class="{ 'is-invalid': errors['attribute.comment'] }"
                >
                </Field>
                <div class="invalid-feedback">
                  {{ errors["attribute.comment"] }}
                </div>
              </div>
            </div>
            <div class="row m-2">
              <div class="col text-start">
                <div class="form-check">
                  <Field
                    class="form-control"
                    id="attribute.to_ids"
                    name="attribute.to_ids"
                    :value="attribute.push"
                    v-model="attribute.to_ids"
                    :class="{ 'is-invalid': errors['attribute.to_ids'] }"
                  >
                    <input
                      class="form-check-input"
                      type="checkbox"
                      v-model="attribute.to_ids"
                    />
                  </Field>
                  <label for="attribute.to_ids"
                    >for intrusion detection system (IDS)</label
                  >
                </div>
              </div>
            </div>
            <div class="row m-2">
              <div class="col text-start">
                <div class="form-check">
                  <Field
                    class="form-control"
                    id="attribute.batch_import"
                    name="attribute.batch_import"
                    :value="attribute.batch_import"
                    v-model="attribute.batch_import"
                    :class="{ 'is-invalid': errors['attribute.batch_import'] }"
                  >
                    <input
                      class="form-check-input"
                      type="checkbox"
                      v-model="attribute.batch_import"
                    />
                  </Field>
                  <label for="attribute.batch_import">batch import</label>
                </div>
              </div>
            </div>
            <div class="row m-2">
              <div class="col text-start">
                <div class="form-check">
                  <Field
                    class="form-control"
                    id="attribute.disable_correlation"
                    name="attribute.disable_correlation"
                    :value="attribute.disable_correlation"
                    v-model="attribute.disable_correlation"
                    :class="{
                      'is-invalid': errors['attribute.disable_correlation'],
                    }"
                  >
                    <input
                      class="form-check-input"
                      type="checkbox"
                      v-model="attribute.disable_correlation"
                    />
                  </Field>
                  <label for="attribute.disable_correlation"
                    >disable correlation</label
                  >
                </div>
              </div>
            </div>
            <div class="row m-2">
              <div class="col col-6 text-start">
                <label for="attribute.first_seen">first seen</label>
                <Datepicker
                  v-model="attribute.first_seen"
                  name="attribute.first_seen"
                  altFormat="Z"
                  dateFormat="U"
                  enableTime
                />
              </div>
              <div class="col col-6 text-start">
                <label for="attribute.last_seen">last seen</label>
                <Datepicker
                  v-model="attribute.last_seen"
                  name="attribute.last_seen"
                  altFormat="Z"
                  dateFormat="U"
                  enableTime
                />
              </div>
            </div>
          </div>
          <div v-if="apiError" class="w-100 alert alert-danger mt-3 mb-3">
            <ApiError :errors="apiError" />
          </div>
          <div class="modal-footer">
            <button
              id="closeModalButton"
              type="button"
              data-bs-dismiss="modal"
              class="btn btn-secondary"
              @click="onClose()"
            >
              Discard
            </button>
            <button
              type="submit"
              class="btn btn-outline-primary"
              :disabled="status.loading"
            >
              <span v-show="status.loading">
                <span
                  class="spinner-border spinner-border-sm"
                  role="status"
                  aria-hidden="true"
                ></span>
              </span>
              <span v-show="!status.loading">Add</span>
            </button>
          </div>
        </div>
      </Form>
    </div>
  </div>
</template>
