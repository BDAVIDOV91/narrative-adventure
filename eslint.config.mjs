import js from '@eslint/js';
import importX from 'eslint-plugin-import-x';
import prettierRecommended from 'eslint-plugin-prettier/recommended';
import unicorn from 'eslint-plugin-unicorn';
import globals from 'globals';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  {
    ignores: ['dist/**', 'node_modules/**', 'data/generated/**', 'venv/**'],
  },
  js.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  unicorn.configs.recommended,
  importX.flatConfigs.recommended,
  importX.flatConfigs.typescript,
  prettierRecommended,
  {
    languageOptions: {
      globals: { ...globals.browser },
      parserOptions: {
        projectService: {
          allowDefaultProject: ['*.mjs', '*.js'],
        },
        tsconfigRootDir: import.meta.dirname,
      },
    },
    settings: {
      'import-x/resolver': {
        typescript: {
          alwaysTryTypes: true,
          project: './tsconfig.json',
        },
      },
    },
    rules: {
      /* kebab-case filenames — pdf_data_extractor_v2 convention */
      'unicorn/filename-case': ['error', { cases: { kebabCase: true } }],

      /* Phaser and Three.js both use abbreviations heavily in their own APIs,
         and "prevent-abbreviations" fights the domain vocabulary constantly. */
      'unicorn/prevent-abbreviations': 'off',
      'unicorn/no-null': 'off',
      'unicorn/prefer-global-this': 'off',
      // Fights ordinary JSDoc and the domain vocabulary; no correctness value here.
      'unicorn/single-line-block-comment-style': 'off',
      'unicorn/name-replacements': 'off',
      'unicorn/consistent-boolean-name': 'off',
      'unicorn/prefer-minimal-ternary': 'off',
      // Colour literals (0xff_d2_6a) are read as byte triples, not number groups.
      'unicorn/numeric-separators-style': 'off',

      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/consistent-type-imports': ['error', { prefer: 'type-imports' }],

      'import-x/order': [
        'error',
        {
          groups: [
            'builtin',
            'external',
            'internal',
            'parent',
            'sibling',
            'index',
            'object',
            'type',
          ],
          'newlines-between': 'always',
          alphabetize: { order: 'asc', caseInsensitive: true },
        },
      ],
      'import-x/no-cycle': 'error',
      'import-x/no-duplicates': 'error',

      /* All player-facing text must resolve through content/bg/ — never a
         literal in a .ts file. console.* is banned so nothing leaks to a
         child's browser console in production. */
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'no-debugger': 'error',
      'no-alert': 'error',
      'prefer-const': 'error',
      'no-var': 'error',
      'object-shorthand': 'error',
    },
  },
  {
    files: ['eslint.config.mjs'],
    rules: {
      'import-x/no-named-as-default': 'off',
      'import-x/no-named-as-default-member': 'off',
    },
  },
  {
    /* Config files run in Node, not the browser. */
    files: ['*.config.ts', '*.config.mjs', 'vite.config.ts', 'vitest.config.ts'],
    languageOptions: { globals: { ...globals.node } },
    rules: { 'import-x/no-nodejs-modules': 'off' },
  },
  {
    /* ops/ is local dev tooling run by Node, never bundled into the game (vite
       builds from src/ only). It wraps third-party code imported at runtime, so
       type-aware rules see only `any` and add noise, not safety. console output
       is the CLI's interface here, not a leak to a child's browser. */
    files: ['ops/**/*.mjs'],
    ...tseslint.configs.disableTypeChecked,
    languageOptions: {
      globals: { ...globals.node },
      parserOptions: { projectService: false, project: null },
    },
    rules: {
      ...tseslint.configs.disableTypeChecked.rules,
      'no-console': 'off',
      'import-x/no-nodejs-modules': 'off',
      // A module that is also a CLI: exports for the test, a guarded main().
      'unicorn/no-exports-in-scripts': 'off',
      // node:test shares server/port state between before() and the tests.
      'unicorn/no-top-level-assignment-in-function': 'off',
      'unicorn/no-await-expression-member': 'off',
    },
  },
);
