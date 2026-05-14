# CHANGELOG

<!-- version list -->

## v2.0.0 (2026-05-14)

### Bug Fixes

- Add default console url value ([#490](https://github.com/rungalileo/galileo-python/pull/490),
  [`7360299`](https://github.com/rungalileo/galileo-python/commit/7360299a4d7fc6078b17910f5e1d194da4cbe53b))

- Add session start handling in new traces client
  ([#543](https://github.com/rungalileo/galileo-python/pull/543),
  [`42b8201`](https://github.com/rungalileo/galileo-python/commit/42b82017c850c575f0daba9d3d09c4876ad4f7a9))

- Add tqdm as explicit required dependency
  ([#492](https://github.com/rungalileo/galileo-python/pull/492),
  [`ac9d5d5`](https://github.com/rungalileo/galileo-python/commit/ac9d5d5710e057e71b10a304dd6a4213ab642563))

- Adjust LogStream.list() to throw NotFoundError when project is unknown
  ([#577](https://github.com/rungalileo/galileo-python/pull/577),
  [`52ab01b`](https://github.com/rungalileo/galileo-python/commit/52ab01ba3457c23f33807bd263d4269a7c04a4b4))

- Attach dataset ground truth fields to OTEL spans
  ([#496](https://github.com/rungalileo/galileo-python/pull/496),
  [`aa3994e`](https://github.com/rungalileo/galileo-python/commit/aa3994eb3209f810ad63660c974ff6438e226ca2))

- Auto-convert non-string metadata values to strings
  ([#488](https://github.com/rungalileo/galileo-python/pull/488),
  [`9b60fa3`](https://github.com/rungalileo/galileo-python/commit/9b60fa3f63d769d245c5d3db62f3509bc32893cf))

- Cannot pass prompt_settings as dict to run_experiment
  ([#527](https://github.com/rungalileo/galileo-python/pull/527),
  [`a32ea66`](https://github.com/rungalileo/galileo-python/commit/a32ea66e3d874c98ff0476b66ca2ed32f0aebf33))

- Clarify error message when GALILEO_API_KEY is not detected
  ([#509](https://github.com/rungalileo/galileo-python/pull/509),
  [`c2bf734`](https://github.com/rungalileo/galileo-python/commit/c2bf73424102cc5d1b52e228bf7f8b506bdf7373))

- Fix unformatted %s placeholder in APIError message in Project.get()
  ([#523](https://github.com/rungalileo/galileo-python/pull/523),
  [`979f2b7`](https://github.com/rungalileo/galileo-python/commit/979f2b78f55ba13ae8935a3ebf359375b5920677))

- Get card fixes ([#552](https://github.com/rungalileo/galileo-python/pull/552),
  [`a1cc7a2`](https://github.com/rungalileo/galileo-python/commit/a1cc7a2998b111f6e168d92fc0b33d4b888f921d))

- Handle legacy token fields from OpenAI usage
  ([#517](https://github.com/rungalileo/galileo-python/pull/517),
  [`6db840f`](https://github.com/rungalileo/galileo-python/commit/6db840fe5b561d42799b87935376d31ca87e828d))

- Missing tasks in hierarchical CrewAI crew traces
  ([#532](https://github.com/rungalileo/galileo-python/pull/532),
  [`6afaa04`](https://github.com/rungalileo/galileo-python/commit/6afaa04e92b0c531ced76b2823a8f98c9ff12fed))

- Move dataset context to decorator to remove otel import from experiments
  ([#502](https://github.com/rungalileo/galileo-python/pull/502),
  [`6e4f193`](https://github.com/rungalileo/galileo-python/commit/6e4f1935a9f069fe443c41074314ff0268d1f870))

- NewSDK: get_version* are [very] confusing
  ([#530](https://github.com/rungalileo/galileo-python/pull/530),
  [`cf606c4`](https://github.com/rungalileo/galileo-python/commit/cf606c4a53dd3c5fc4b769cfe6eeb7516b708c96))

- Prioritize experiment over logstream in OTEL export
  ([#498](https://github.com/rungalileo/galileo-python/pull/498),
  [`12c736a`](https://github.com/rungalileo/galileo-python/commit/12c736a034cbda50b3675b1fe5ffa88ab199cd6f))

- Python SDK tests often hang ([#531](https://github.com/rungalileo/galileo-python/pull/531),
  [`7dff69d`](https://github.com/rungalileo/galileo-python/commit/7dff69ddd48fc77aa554fc724ce97e376f943385))

- Raise consistent ResourceNotFoundError when project cannot be resolved
  ([#510](https://github.com/rungalileo/galileo-python/pull/510),
  [`ec6e2d0`](https://github.com/rungalileo/galileo-python/commit/ec6e2d039219f2027d70f7fc237eddc2de7c3cf8))

- Raise error when extend/generate job fails silently
  ([#528](https://github.com/rungalileo/galileo-python/pull/528),
  [`d7b9da1`](https://github.com/rungalileo/galileo-python/commit/d7b9da1c1b0c40a70efe5f205a4a557478999b70))

- Regression issues on experiments ([#511](https://github.com/rungalileo/galileo-python/pull/511),
  [`b7cc9bd`](https://github.com/rungalileo/galileo-python/commit/b7cc9bdc10591ed4b7e9ca49874fd1612546974a))

- Resolve OpenAI test failures when Azure env vars are set
  ([#540](https://github.com/rungalileo/galileo-python/pull/540),
  [`5322d63`](https://github.com/rungalileo/galileo-python/commit/5322d6362d70f2089e2ed82eb507567c0d856a86))

- Schema patches ([#573](https://github.com/rungalileo/galileo-python/pull/573),
  [`05a8d7f`](https://github.com/rungalileo/galileo-python/commit/05a8d7f4304e146db60e13e3e997ceea795bd14c))

- The filter schema patches ([#568](https://github.com/rungalileo/galileo-python/pull/568),
  [`da22838`](https://github.com/rungalileo/galileo-python/commit/da228383d9b64eddaddfba298876a2ec62430aae))

- Url ([#571](https://github.com/rungalileo/galileo-python/pull/571),
  [`bc36762`](https://github.com/rungalileo/galileo-python/commit/bc367626d1160c93b791f28eb333579ab409ce35))

- **config**: Extend auth guard to recognize all supported auth methods
  ([#579](https://github.com/rungalileo/galileo-python/pull/579),
  [`83488f6`](https://github.com/rungalileo/galileo-python/commit/83488f62420c4e9949033d14f4e477b32f24d827))

- **dataset**: Extend now adds generated rows to the existing dataset
  ([#544](https://github.com/rungalileo/galileo-python/pull/544),
  [`2f0db14`](https://github.com/rungalileo/galileo-python/commit/2f0db1432cdc8c55fc7b570070dd560b0634b246))

- **dataset**: Normalize ground_truth to output in add_rows
  ([#545](https://github.com/rungalileo/galileo-python/pull/545),
  [`c262a27`](https://github.com/rungalileo/galileo-python/commit/c262a27c8a850f8d641056a1473cd7ee004dddc7))

- **datasets**: Adjust default model alias name
  ([#535](https://github.com/rungalileo/galileo-python/pull/535),
  [`95a4e45`](https://github.com/rungalileo/galileo-python/commit/95a4e459f65fca9b63f8cff5856f233e741d6e68))

- **datasets**: Preserve all prompt_settings fields in extend_dataset
  ([#549](https://github.com/rungalileo/galileo-python/pull/549),
  [`4b290c8`](https://github.com/rungalileo/galileo-python/commit/4b290c81106314b1a64995e7bb603f646b21c4a7))

- **datasets**: Remap 'output' to 'ground_truth' in get_content() response
  ([#555](https://github.com/rungalileo/galileo-python/pull/555),
  [`be7666d`](https://github.com/rungalileo/galileo-python/commit/be7666dda4c88af3dc0673d85768bb220a97911f))

- **deprecations**: Remove @deprecated decorators from legacy SDK functions
  ([#562](https://github.com/rungalileo/galileo-python/pull/562),
  [`6c0d200`](https://github.com/rungalileo/galileo-python/commit/6c0d200a9b9bf3af332cb296df4e939424d8d434))

- **deps**: Bump pyjwt to >=2.12.0 (fixes CVE-2026-32597 / GHSA-752w-5fwx-jx9f)
  ([#558](https://github.com/rungalileo/galileo-python/pull/558),
  [`548addf`](https://github.com/rungalileo/galileo-python/commit/548addf39b447c973e4700b5870fa5376f7ad203))

- **deps**: Upgrade openai to 2.x and litellm to >=1.83.0 (fixes CVE GHSA-69x8-hrgq-fjj8)
  ([#557](https://github.com/rungalileo/galileo-python/pull/557),
  [`f5e90da`](https://github.com/rungalileo/galileo-python/commit/f5e90dae720a675f79031f3157c66edd211b5593))

- **docs**: Update span docstrings with accurate input formats
  ([#541](https://github.com/rungalileo/galileo-python/pull/541),
  [`63197c1`](https://github.com/rungalileo/galileo-python/commit/63197c15695c2d3071f3256b07c996cf2c56fe96))

- **errors**: Context-aware project-not-found error messages
  ([#569](https://github.com/rungalileo/galileo-python/pull/569),
  [`0c8efb8`](https://github.com/rungalileo/galileo-python/commit/0c8efb88af614b5326e48b294759660f4bf5ed8a))

- **experiment**: Make prompt optional in Experiment.__init__
  ([#563](https://github.com/rungalileo/galileo-python/pull/563),
  [`e2ad2c2`](https://github.com/rungalileo/galileo-python/commit/e2ad2c240b4b7c61a5b887eb463770add08dcdc1))

- **experiment**: Preserve user prompt_settings when overriding model
  ([#547](https://github.com/rungalileo/galileo-python/pull/547),
  [`50987ce`](https://github.com/rungalileo/galileo-python/commit/50987cee8bacce2949f615bfcc2ff625add7173d))

- **experiment**: Reset _run_result_consumed flag in create()
  ([#548](https://github.com/rungalileo/galileo-python/pull/548),
  [`6ea5380`](https://github.com/rungalileo/galileo-python/commit/6ea538034ac2b7164e4cd45dad709a0c73b52fc5))

- **experiments,jobs**: Surface validation errors on invalid model alias
  ([#550](https://github.com/rungalileo/galileo-python/pull/550),
  [`74443ad`](https://github.com/rungalileo/galileo-python/commit/74443add47ec8880dfad2a18d235c290d59d0932))

- **log_stream**: Convert ProjectsAPIException to ResourceNotFoundError in get/list
  ([#561](https://github.com/rungalileo/galileo-python/pull/561),
  [`4a45976`](https://github.com/rungalileo/galileo-python/commit/4a4597684b8bfb1780f59e24d15b5656b27277f7))

- **logger**: Add explicit str to start_trace input type hints and docstrings
  ([#574](https://github.com/rungalileo/galileo-python/pull/574),
  [`b186595`](https://github.com/rungalileo/galileo-python/commit/b186595f8c3ee3a25a8a11e3e8574a644723b457))

- **logger**: Add list[dict] to start_trace input docs
  ([#565](https://github.com/rungalileo/galileo-python/pull/565),
  [`2cbf848`](https://github.com/rungalileo/galileo-python/commit/2cbf8487dae71d76244949d29984f5253b610b17))

- **step_type**: Add CONTROL to StepType enum
  ([#570](https://github.com/rungalileo/galileo-python/pull/570),
  [`dd17a21`](https://github.com/rungalileo/galileo-python/commit/dd17a21335de74a845c47c22934eed2e2b8b17fc))

- **validation**: Handle plain-string detail in HTTPValidationError
  ([#564](https://github.com/rungalileo/galileo-python/pull/564),
  [`2f67cfb`](https://github.com/rungalileo/galileo-python/commit/2f67cfbb1d5643f9faf32980afd4e48da8f338b1))

### Chores

- Bump galileo-core to ^4.1.2 ([#499](https://github.com/rungalileo/galileo-python/pull/499),
  [`f0a561a`](https://github.com/rungalileo/galileo-python/commit/f0a561a86fee61f299213ccba19f5a75e2c70da5))

- Bump galileo-core to ^4.2.1 ([#507](https://github.com/rungalileo/galileo-python/pull/507),
  [`66e86cd`](https://github.com/rungalileo/galileo-python/commit/66e86cd758f08a76fee6904a149bf57d7e660e9b))

- Migrating remaining files to root ([#512](https://github.com/rungalileo/galileo-python/pull/512),
  [`c86c53a`](https://github.com/rungalileo/galileo-python/commit/c86c53a4f7446598c7aed2459a5ba133bcadea60))

- Release version 2.1.2
  ([`edecb41`](https://github.com/rungalileo/galileo-python/commit/edecb412e4e303d2c1d7ab17154222e12ec703b3))

- Release version 2.1.3
  ([`207c9ce`](https://github.com/rungalileo/galileo-python/commit/207c9ce931269b4cf482a23280bf84d70a982e6f))

- Remove CODEOWNERS ([#533](https://github.com/rungalileo/galileo-python/pull/533),
  [`354491b`](https://github.com/rungalileo/galileo-python/commit/354491b828aae4a83d86f7db45d0aafd8e63cacb))

- Update CONTRIBUTING.md ([#582](https://github.com/rungalileo/galileo-python/pull/582),
  [`9435453`](https://github.com/rungalileo/galileo-python/commit/943545377df0200cf2fcf4c4ea8500ed6b47eff8))

- Update dev environment to recommend Python 3.13
  ([#518](https://github.com/rungalileo/galileo-python/pull/518),
  [`4b197ab`](https://github.com/rungalileo/galileo-python/commit/4b197ab8bc4c94120f852d1ae5161af46f49aba1))

- Update ruff target-version and fix mypy pre-commit hook
  ([#536](https://github.com/rungalileo/galileo-python/pull/536),
  [`4b6bffb`](https://github.com/rungalileo/galileo-python/commit/4b6bffbf9e54f96479fe2308e5f0ac100ec55594))

- **release**: Galileo-a2a v1.0.0
  ([`bc515b3`](https://github.com/rungalileo/galileo-python/commit/bc515b346a00071f1ed2c38dba17db321350a3b6))

- **release**: V1.48.0
  ([`bdcdede`](https://github.com/rungalileo/galileo-python/commit/bdcdede246a5c885e3afd8c8d48f02a3f3630ed0))

- **release**: V1.49.0
  ([`5a7c747`](https://github.com/rungalileo/galileo-python/commit/5a7c74796e3063f8fe255acccfb98db7cc19488c))

- **release**: V1.49.1
  ([`beb1a4a`](https://github.com/rungalileo/galileo-python/commit/beb1a4acb038c7f207619f01591d013815a06b76))

- **release**: V1.49.2
  ([`459457d`](https://github.com/rungalileo/galileo-python/commit/459457d22710a00acf796984b9e9972d2c3ec6f3))

- **release**: V1.50.0
  ([`a8ac26f`](https://github.com/rungalileo/galileo-python/commit/a8ac26ff4c952e2385a77a4ae06b6cc452c66ebd))

- **release**: V1.50.1
  ([`30b381a`](https://github.com/rungalileo/galileo-python/commit/30b381ad496d2c8631924977ee49c1458bda3897))

- **release**: V1.51.0
  ([`a6dadc6`](https://github.com/rungalileo/galileo-python/commit/a6dadc6b25dddb81082e4b02cefa9f6a24b6089e))

- **release**: V2.0.0
  ([`0dcb7d9`](https://github.com/rungalileo/galileo-python/commit/0dcb7d9a1139380b4e9f3c6bc14a5041e28f8ee4))

- **release**: V2.1.0
  ([`eedf91f`](https://github.com/rungalileo/galileo-python/commit/eedf91fc674d341e8cfce620c19ad806cc895adb))

- **release**: V2.1.1
  ([`ba8c8d2`](https://github.com/rungalileo/galileo-python/commit/ba8c8d2e94b1bc5261ce2feb1370d9eabef7f4b4))

- **release**: V2.2.0
  ([`10a8a90`](https://github.com/rungalileo/galileo-python/commit/10a8a90745160ad43779c860aa83a078712f6f13))

### Features

- Add Agent Control target helper ([#581](https://github.com/rungalileo/galileo-python/pull/581),
  [`8ef084f`](https://github.com/rungalileo/galileo-python/commit/8ef084ff92e1108927cef88dfe5f563b2efe6788))

- Add agentcontrol logger bridge ([#566](https://github.com/rungalileo/galileo-python/pull/566),
  [`861c2e3`](https://github.com/rungalileo/galileo-python/commit/861c2e3bfe43c1a4cab1501884c3cd9efe0c4ce7))

- Add metric_aggregates + experiment_columns, deprecate aggregate_metrics
  ([#578](https://github.com/rungalileo/galileo-python/pull/578),
  [`9b3c424`](https://github.com/rungalileo/galileo-python/commit/9b3c42403fb943a40c24ecbfa7fe35b1224c6eb9))

- Add proto-plus message serialization support in EventSerializer…
  ([#485](https://github.com/rungalileo/galileo-python/pull/485),
  [`5cabda5`](https://github.com/rungalileo/galileo-python/commit/5cabda5557020bf5d345e8faddbbd733aad4b42c))

- Add support for serializing WorkflowSpan input and output
  ([#472](https://github.com/rungalileo/galileo-python/pull/472),
  [`ed49115`](https://github.com/rungalileo/galileo-python/commit/ed491150331ec93a19471d582e9171ba278a4913))

- Add support for ToolSpan attributes
  ([#475](https://github.com/rungalileo/galileo-python/pull/475),
  [`aa8ba2e`](https://github.com/rungalileo/galileo-python/commit/aa8ba2eea2d1cf978156c493980abd068bbdd96f))

- Creating custom input and output types for multimodal ingestion
  ([#500](https://github.com/rungalileo/galileo-python/pull/500),
  [`3685658`](https://github.com/rungalileo/galileo-python/commit/368565852e04f00247836fcdba339112e71ce5e2))

- Harden a2a distributed tracing and improve test coverage
  ([#546](https://github.com/rungalileo/galileo-python/pull/546),
  [`263a79b`](https://github.com/rungalileo/galileo-python/commit/263a79b383f5b4753911535b355ec3ba1a90a179))

- Implement google a2a instrumentor ([#529](https://github.com/rungalileo/galileo-python/pull/529),
  [`ca24de6`](https://github.com/rungalileo/galileo-python/commit/ca24de66ef93d610f5e0e719b67c1ed2f08f830a))

- Implement Metric.update() via PATCH /scorers/{id}
  ([#505](https://github.com/rungalileo/galileo-python/pull/505),
  [`f181ab6`](https://github.com/rungalileo/galileo-python/commit/f181ab69d3bf7d56f865ef70cc7aabb4527dd08f))

- Implement Project.save() and Dataset.save()
  ([#503](https://github.com/rungalileo/galileo-python/pull/503),
  [`5d473ed`](https://github.com/rungalileo/galileo-python/commit/5d473edf0e4b27fa593eacc68b9433e17ddf309b))

- Implement Prompt.save() with automatic dirty tracking for name changes
  ([#504](https://github.com/rungalileo/galileo-python/pull/504),
  [`e8cc58f`](https://github.com/rungalileo/galileo-python/commit/e8cc58f6f00dd71418bf601899da3fbce287fd8f))

- Improve metric naming conventions and optimize scorer retrieval
  ([#522](https://github.com/rungalileo/galileo-python/pull/522),
  [`65e28c7`](https://github.com/rungalileo/galileo-python/commit/65e28c77ab983af1a4cc258392dd08f408331136))

- Serialize trace output in distributed mode decorator path
  ([#514](https://github.com/rungalileo/galileo-python/pull/514),
  [`444ce9b`](https://github.com/rungalileo/galileo-python/commit/444ce9be5dece6fa352c321246e6a7530b6493e2))

- Support crewai 1.9.3 ([#484](https://github.com/rungalileo/galileo-python/pull/484),
  [`dba40f6`](https://github.com/rungalileo/galileo-python/commit/dba40f62d09d5e1e820082b732b14da6d23a76a8))

- Support experiment groups (V1) ([#575](https://github.com/rungalileo/galileo-python/pull/575),
  [`46c1b35`](https://github.com/rungalileo/galileo-python/commit/46c1b35832468a30e8912a2a06244756b6a68856))

- Support generated-output flow in run_experiment (no prompt_temp…
  ([#486](https://github.com/rungalileo/galileo-python/pull/486),
  [`222acf8`](https://github.com/rungalileo/galileo-python/commit/222acf8fd3300773058052d6f029e31af2140ecc))

- Switch run_experiment to trigger=True for generated output flow
  ([#497](https://github.com/rungalileo/galileo-python/pull/497),
  [`837d9b5`](https://github.com/rungalileo/galileo-python/commit/837d9b546cac3b47db824b13df5bf4585156bed0))

- **experiments**: Add on_error callback to flush and experiment run
  ([#537](https://github.com/rungalileo/galileo-python/pull/537),
  [`e08596c`](https://github.com/rungalileo/galileo-python/commit/e08596c6ac7ce7dd4a708110d8148fd35363d5cc))

- **langchain**: Add multimodal content support to LangChain handler
  ([#515](https://github.com/rungalileo/galileo-python/pull/515),
  [`fb6c1a1`](https://github.com/rungalileo/galileo-python/commit/fb6c1a1f87c94fb396ed19e795cc4712315ff313))

- **log-stream**: Add limit parameter to LogStream.list()
  ([#580](https://github.com/rungalileo/galileo-python/pull/580),
  [`cccd15e`](https://github.com/rungalileo/galileo-python/commit/cccd15e4370aeedfe64b9d4d9a37cd84c693c5ec))

- **logger**: Validate input types in start_trace
  ([#539](https://github.com/rungalileo/galileo-python/pull/539),
  [`e07ab69`](https://github.com/rungalileo/galileo-python/commit/e07ab69290f1a67229bca59d4f3ab63961fbaff0))

### Refactoring

- Add @deprecated decorators to legacy service functions in datasets, experiments, prompts,
  log_streams ([#524](https://github.com/rungalileo/galileo-python/pull/524),
  [`546e00f`](https://github.com/rungalileo/galileo-python/commit/546e00fa1d00f9a5f25b55aabbfe0343733417ed))

- Adding deprecated on __future__ re export
  ([#525](https://github.com/rungalileo/galileo-python/pull/525),
  [`69d0c22`](https://github.com/rungalileo/galileo-python/commit/69d0c2207cb13393510ddb3002e8e38e62aa7392))

- Move tests from tests/future/ to tests/ directory
  ([#526](https://github.com/rungalileo/galileo-python/pull/526),
  [`48bc50c`](https://github.com/rungalileo/galileo-python/commit/48bc50cbee9819048a37b834ae9a6133b171dced))

- Moving project.py to root, away from __future__
  ([#506](https://github.com/rungalileo/galileo-python/pull/506),
  [`1dd4b4c`](https://github.com/rungalileo/galileo-python/commit/1dd4b4c4eaca11ffb33e9478da38b143cb4fb4b2))

- Streamline project and logstream resolution in GalileoOTLPE…
  ([#493](https://github.com/rungalileo/galileo-python/pull/493),
  [`8be1413`](https://github.com/rungalileo/galileo-python/commit/8be141376bca9114d27492b5eea503812da07dcc))


## v1.0.0 (2026-02-23)

### Bug Fixes

- Also send metadata on async handler
  ([#476](https://github.com/rungalileo/galileo-python/pull/476),
  [`7a85819`](https://github.com/rungalileo/galileo-python/commit/7a8581976c00499bffc36b5d03e95f04d4e12bab))

- Normalize ground_truth to output in create_dataset
  ([#481](https://github.com/rungalileo/galileo-python/pull/481),
  [`545073a`](https://github.com/rungalileo/galileo-python/commit/545073acc8dd59c2d656f36ca11bfd8b46319686))

- **handlers**: Pass ingestion_hook through handler → logger chain
  ([#479](https://github.com/rungalileo/galileo-python/pull/479),
  [`4cd3c10`](https://github.com/rungalileo/galileo-python/commit/4cd3c106aca157ae95d5dbbd8ce09fa793eaf44c))

### Chores

- Change crew ai imports to be lazy ([#477](https://github.com/rungalileo/galileo-python/pull/477),
  [`d1f987a`](https://github.com/rungalileo/galileo-python/commit/d1f987a530e966f9134b8c6f9f2fdbc19bc68b9b))

- **release**: Galileo-adk v1.0.0
  ([`0e364eb`](https://github.com/rungalileo/galileo-python/commit/0e364eb1158d2e6e920c5afa519a26fe35befcac))

- **release**: V1.46.1
  ([`25c51cd`](https://github.com/rungalileo/galileo-python/commit/25c51cdae90ffa3f165a49e1b7046e2a2f382120))

- **release**: V1.46.2
  ([`17c8b0f`](https://github.com/rungalileo/galileo-python/commit/17c8b0f3ec5db18d859c9728aa2d64354d893624))

- **release**: V1.47.0
  ([`a3106fd`](https://github.com/rungalileo/galileo-python/commit/a3106fd6cb8e68c7bed73516a8881bc1837ee8b4))

### Features

- Allow session metadata tagging ([#480](https://github.com/rungalileo/galileo-python/pull/480),
  [`114e24d`](https://github.com/rungalileo/galileo-python/commit/114e24db31eef7a16f966eb6c9238f13c88a66ca))

- Galileo adk to natively support custom retriever tools
  ([#482](https://github.com/rungalileo/galileo-python/pull/482),
  [`f11138a`](https://github.com/rungalileo/galileo-python/commit/f11138aaf5dd944f4cd3b5dfe486755e7c1c65a1))


## v1.0.0-beta.1 (2026-02-11)

- Initial Release
