module.exports = {
  env: { node: true, jest: true },
  root: true,
  parser: "@typescript-eslint/parser",
  plugins: ["@typescript-eslint"],
  extends: ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
  rules: {
    "@typescript-eslint/no-unused-vars": "error",
    "no-undef": "error",
    "prefer-const": "error",
    "no-console": "warn",
  },
  ignorePatterns: ["dist", "examples", "node_modules"],
};
