# CHANGELOG


## v0.1.0 (2025-03-14)

### Bug Fixes

- Adding init, reset, and flush_all methods to galileo_context, adding tests, fixing existing tests
  ([#28](https://github.com/rungalileo/galileo-python/pull/28),
  [`569d1d0`](https://github.com/rungalileo/galileo-python/commit/569d1d07686f54b434081f1f79fe5c318e8873f9))

- Change job name according to new api version
  ([#52](https://github.com/rungalileo/galileo-python/pull/52),
  [`9c9352d`](https://github.com/rungalileo/galileo-python/commit/9c9352dc51f8591a33cf411d580707bfc18162d8))

- Fixing an issue with parsing OpenAI tool calls outputs
  ([#36](https://github.com/rungalileo/galileo-python/pull/36),
  [`55c0fe4`](https://github.com/rungalileo/galileo-python/commit/55c0fe44445b6a3b3858978853dd48057bc0452f))

- Fixing get log_stream by name ([#40](https://github.com/rungalileo/galileo-python/pull/40),
  [`2571024`](https://github.com/rungalileo/galileo-python/commit/257102433d2ab765a11526481d6b2f7c729b6b61))

- Output parsing for retriever spans ([#34](https://github.com/rungalileo/galileo-python/pull/34),
  [`c87f926`](https://github.com/rungalileo/galileo-python/commit/c87f9268b8ef681ed8535ec0aad5e5b612a71243))

- Serialization of non-serialized types or classes
  ([#48](https://github.com/rungalileo/galileo-python/pull/48),
  [`39d7611`](https://github.com/rungalileo/galileo-python/commit/39d761164b4659f4313cbe05bcf0246371520bbe))

- Serializing trace, workflow, and tool span inputs and outputs
  ([#41](https://github.com/rungalileo/galileo-python/pull/41),
  [`e54cb95`](https://github.com/rungalileo/galileo-python/commit/e54cb9585ffbf6cdbb9e553f76c1fc836b37e36b))

- Set min Python version for ruff to py39
  ([#23](https://github.com/rungalileo/galileo-python/pull/23),
  [`fcfc0d1`](https://github.com/rungalileo/galileo-python/commit/fcfc0d11937bcde62f38d0e21c2319afa9af3d8f))

- Typo inside ./scripts/auto-generate-api-client.sh
  ([#32](https://github.com/rungalileo/galileo-python/pull/32),
  [`252c061`](https://github.com/rungalileo/galileo-python/commit/252c061d7798cef822b24dc6819f49e5864a7bf9))

- Update add_llm_span example ([#39](https://github.com/rungalileo/galileo-python/pull/39),
  [`e01838f`](https://github.com/rungalileo/galileo-python/commit/e01838ffe95181133c455f21bc57cc5f1aacd297))

### Chores

- Add missing keys to `pyproject.toml` ([#57](https://github.com/rungalileo/galileo-python/pull/57),
  [`500ac21`](https://github.com/rungalileo/galileo-python/commit/500ac21f6201c738a59546b8d602ca947575992f))

- Fix path to `__init__` ([#61](https://github.com/rungalileo/galileo-python/pull/61),
  [`8d6425d`](https://github.com/rungalileo/galileo-python/commit/8d6425df53510f67f543192e014f694a894651f3))

- Remove js dir and files ([#56](https://github.com/rungalileo/galileo-python/pull/56),
  [`962ae5d`](https://github.com/rungalileo/galileo-python/commit/962ae5da831da3d10f5748aa1333ef6e6fe1b6fe))

- Set version field in `pyproject.toml` correctly
  ([#60](https://github.com/rungalileo/galileo-python/pull/60),
  [`1560b76`](https://github.com/rungalileo/galileo-python/commit/1560b7615df8bf0320ab531bcd3f87c5fa41495d))

- Setup repo + package similarly to our other Python repos
  ([#25](https://github.com/rungalileo/galileo-python/pull/25),
  [`4daac02`](https://github.com/rungalileo/galileo-python/commit/4daac020776875d2d1e174b300f558f68448671e))

- **deps**: Bump `galileo-core` to v3.2+
  ([#29](https://github.com/rungalileo/galileo-python/pull/29),
  [`ed234e3`](https://github.com/rungalileo/galileo-python/commit/ed234e3495281409095db3243cff8b01143cd41d))

- **deps**: Bump codecov/codecov-action from 5.3.1 to 5.4.0
  ([#42](https://github.com/rungalileo/galileo-python/pull/42),
  [`41d7955`](https://github.com/rungalileo/galileo-python/commit/41d79556106db802b2013b40bbf7ac2a65b5899f))

- **deps**: Bump python-semantic-release/python-semantic-release from 9.20.0 to 9.21.0
  ([#43](https://github.com/rungalileo/galileo-python/pull/43),
  [`95543ce`](https://github.com/rungalileo/galileo-python/commit/95543cec5afb5df96b75439ab7888065f805c4e8))

### Continuous Integration

- Bump python-semantic-release/python-semantic-release from 9.17.0 to 9.20.0
  ([#26](https://github.com/rungalileo/galileo-python/pull/26),
  [`ac9aaab`](https://github.com/rungalileo/galileo-python/commit/ac9aaab3539e1ff3e1603ea8371064e6913ddf36))

### Documentation

- Add reference docs to the more client-facing pages
  ([#37](https://github.com/rungalileo/galileo-python/pull/37),
  [`08b3457`](https://github.com/rungalileo/galileo-python/commit/08b3457d9957523d77e480b4c2dce9e63bb0f5f6))

Co-authored-by: ajaynayak <ajaynayak@gmail.com>

- Add small note about poetry shell ([#12](https://github.com/rungalileo/galileo-python/pull/12),
  [`d598aae`](https://github.com/rungalileo/galileo-python/commit/d598aae0fb61c700e9ea56fdeb72154aeb343aea))

### Features

- Add streaming support to openai wrapper
  ([#31](https://github.com/rungalileo/galileo-python/pull/31),
  [`78687c7`](https://github.com/rungalileo/galileo-python/commit/78687c72cbc4ac10df5630209ffe9b09a4dd56f2))

- Adding a client-type header to all requests
  ([#54](https://github.com/rungalileo/galileo-python/pull/54),
  [`764ee2d`](https://github.com/rungalileo/galileo-python/commit/764ee2d00cb3493304c2d1af51ce1f1b97a5d6e1))

- Adding a way to conclude all spans in a trace; restoring defaults in the decorator
  ([#35](https://github.com/rungalileo/galileo-python/pull/35),
  [`130fe02`](https://github.com/rungalileo/galileo-python/commit/130fe0218f2df201b86366959b165034a44c74e9))

- Catch and handle errors throughout the client
  ([#46](https://github.com/rungalileo/galileo-python/pull/46),
  [`d6a82ee`](https://github.com/rungalileo/galileo-python/commit/d6a82eed09b1923d8d25c792e804857419b62a98))

- Changes to support the new core logging schemas
  ([#30](https://github.com/rungalileo/galileo-python/pull/30),
  [`a2c6ca8`](https://github.com/rungalileo/galileo-python/commit/a2c6ca85efb7ad1d5e1e581219c88c91484fd3b6))

Changes to the client based on the following core and api changes: rungalileo/core#232
  rungalileo/api#3489

There were some DX changes I made in this PR that will need to get moved to core: - renaming
  user_metadata to metadata for the logging functions - allowing more flexible types to be used for
  documents in the add_retriever_span() method. The current traces_logger method is too restrictive
  (forces a user to specify a list of dicts or a list of Documents, else throws an error). Since
  we're using function decorators, we need to be more permissive of method outputs which will map to
  the retriever documents field.

- Decorator should create trace but reraise original exception
  ([#45](https://github.com/rungalileo/galileo-python/pull/45),
  [`d3dbb7a`](https://github.com/rungalileo/galileo-python/commit/d3dbb7a0cb2a6e37c0684ec18cd55ee1113e173f))

- Implement get/create for prompt templates
  ([#49](https://github.com/rungalileo/galileo-python/pull/49),
  [`c647da3`](https://github.com/rungalileo/galileo-python/commit/c647da3bd1ac44033b493d7ca7f8ef70877a7e68))

- Langchain callback ([#44](https://github.com/rungalileo/galileo-python/pull/44),
  [`b6dd9a3`](https://github.com/rungalileo/galileo-python/commit/b6dd9a3514b3dba7e2a48beff42342b352b2e60e))

- Replace app.galileo.ai with api.galileo.ai if users specify it incorrectly
  ([#53](https://github.com/rungalileo/galileo-python/pull/53),
  [`9a7ac9e`](https://github.com/rungalileo/galileo-python/commit/9a7ac9e623808341c9bf72ffc58543943bf6d27f))

- Run experiment with a runner function and hosted metrics
  ([#58](https://github.com/rungalileo/galileo-python/pull/58),
  [`5c37ff7`](https://github.com/rungalileo/galileo-python/commit/5c37ff7516d020a8195c23fe30907e9839f2d9fe))

Co-authored-by: Andrii Soldatenko <ubuntu@ip-172-31-28-161.eu-central-1.compute.internal>

Co-authored-by: ajaynayak <ajaynayak@gmail.com>

- Run experiment with run_prompt and hosted metrics
  ([#50](https://github.com/rungalileo/galileo-python/pull/50),
  [`c78908f`](https://github.com/rungalileo/galileo-python/commit/c78908f699006311a1249c0341ed9f34f589dcde))

- Updating the readme and pyproject for release
  ([#59](https://github.com/rungalileo/galileo-python/pull/59),
  [`867a327`](https://github.com/rungalileo/galileo-python/commit/867a327e92395451feb3e2a76b301a10a3cb8f99))

### Refactoring

- Removing `project` and `log_stream` from the `log` decorator
  ([#55](https://github.com/rungalileo/galileo-python/pull/55),
  [`d348dbd`](https://github.com/rungalileo/galileo-python/commit/d348dbdc1dd23595c8bfbaee736112681e11ea21))

### Testing

- Add tests to emulate openai errors and galileo api errors
  ([#38](https://github.com/rungalileo/galileo-python/pull/38),
  [`16f73bb`](https://github.com/rungalileo/galileo-python/commit/16f73bb6f63a755a8d4ee3a907b4d938a22519f9))

- Adding unit tests for openai wrapper ([#27](https://github.com/rungalileo/galileo-python/pull/27),
  [`fdc15d1`](https://github.com/rungalileo/galileo-python/commit/fdc15d144b1e10199d64d3d5bc706f7da80e2a94))

- Dont ignore async test ([#33](https://github.com/rungalileo/galileo-python/pull/33),
  [`6f75fa8`](https://github.com/rungalileo/galileo-python/commit/6f75fa8e134cc1e8ec82e2856680e354386b5414))
