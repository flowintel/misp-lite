<script setup>
import { Field } from "vee-validate";

const props = defineProps(["name", "selected", "errors"]);
const emit = defineEmits(["disable_correlation-updated"]);

function handleSelectChange(event) {
  emit("disable_correlation-updated", event.target.value);
}
</script>

<template>
  <Field
    class="form-control"
    :name="name"
    :class="{ 'is-invalid': errors }"
    as="select"
    @change="handleSelectChange"
    :value="props.selected"
  >
    <option value="true">true</option>
    <option value="false">false</option>
  </Field>
</template>
