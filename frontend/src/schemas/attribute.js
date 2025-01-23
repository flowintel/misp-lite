import * as Yup from "yup";
import ipRegex from "ip-regex";

export const AttributeSchema = Yup.object().shape({
  attribute: Yup.object().shape({
    value: Yup.string().required(),
    timestamp: Yup.number(),
    distribution: Yup.number().required(),
    disable_correlation: Yup.boolean().required(),
    category: Yup.string().required(),
    type: Yup.string().required(),
    first_seen: Yup.string(),
    last_seen: Yup.string(),
  }),
});

export const getAttributeTypeValidationSchema = (type) => {
  if (type === "ip-src" || type === "ip-dst") {
    return AttributeSchema.concat(
      Yup.object().shape({
        attribute: Yup.object().shape({
          value: Yup.string()
            .matches(ipRegex({ exact: true }), "Invalid IP address.")
            .required(),
        }),
      })
    );
  }

  if (type === "email") {
    return AttributeSchema.concat(
      Yup.object().shape({
        attribute: Yup.object().shape({
          value: Yup.string().email().required(),
        }),
      })
    );
  }

  if (type === "url") {
    return AttributeSchema.concat(
      Yup.object().shape({
        attribute: Yup.object().shape({
          value: Yup.string().url().required(),
        }),
      })
    );
  }

  return AttributeSchema;
};
