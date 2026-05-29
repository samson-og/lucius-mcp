# Story 11.1: Flatten Telemetry Event Names

Status: review

## Story

As a Lucius maintainer,
I want telemetry events to use flat top-level names such as `startup`, `tool_use`, and `tool_error`,
so that downstream dashboards can group events consistently while keeping the same runtime properties in the payload.

## Acceptance Criteria

1. **Startup event name is flat**
   - **Given** Lucius emits a startup telemetry event
   - **When** telemetry is enabled
   - **Then** the event name is exactly `startup`
   - **And** the payload still includes `deployment_method`, `mcp_mode`, `server_version`, and the rest of the current startup properties.

2. **Successful tool event name is flat**
   - **Given** Lucius emits a successful tool telemetry event
   - **When** any tool finishes successfully
   - **Then** the event name is exactly `tool_use`
   - **And** the payload still includes `tool_name`, `outcome`, `duration_bucket`, and the current runtime context fields.

3. **Failed tool event name is flat**
   - **Given** Lucius emits a failed tool telemetry event
   - **When** validation, auth, API, or unexpected failures occur
   - **Then** the event name is exactly `tool_error`
   - **And** the payload still includes `tool_name`, `outcome`, and `error_category`
   - **And** the implementation does not add replacement sublevels such as `tool_error.validation`.

4. **Existing properties remain queryable**
   - **Given** dashboards or tests need deployment method, tool identity, or error class
   - **When** they read the payload
   - **Then** those dimensions are still available as properties
   - **And** no existing telemetry property is removed solely because the event name was flattened.

5. **Tests and docs reflect the new contract**
   - **Given** maintainers review the telemetry behavior
   - **When** they read docs or run tests
   - **Then** docs explicitly describe the flat event taxonomy
   - **And** unit, integration, and e2e tests assert the new names while preserving payload assertions.

## Tasks / Subtasks

- [x] **Task 1: Flatten event names in the telemetry service** (AC: 1, 2, 3, 4)
  - [x] 1.1 Change startup event emission in `src/services/telemetry_service.py` from `startup.<deployment_method>` to `startup`.
  - [x] 1.2 Change successful tool event emission from `tool_use.<tool_name>` to `tool_use`.
  - [x] 1.3 Change failed tool event emission from `tool_error.<category>.<tool_name>` to `tool_error`.
  - [x] 1.4 Keep `deployment_method`, `tool_name`, and `error_category` in the payload unchanged.

- [x] **Task 2: Update automated coverage** (AC: 1, 2, 3, 4, 5)
  - [x] 2.1 Update `tests/unit/test_telemetry_service.py` for flat startup/tool event names.
  - [x] 2.2 Update `tests/integration/test_telemetry_integration.py` for flat event names.
  - [x] 2.3 Update `tests/e2e/test_telemetry_collection_e2e.py` to select events by flat name plus payload fields.

- [x] **Task 3: Update telemetry docs** (AC: 5)
  - [x] 3.1 Update `docs/telemetry.md` to document the flat event taxonomy and note that dimensionality stays in payload fields.

## Dev Notes

### Scope

- This is a telemetry contract simplification only.
- Do not remove or rename existing payload properties.
- Do not change opt-out, hashing, transport, or error-swallowing behavior.

### References

- [Source: specs/project-planning-artifacts/epics.md#Epic 11]
- [Source: specs/implementation-artifacts/8-5-implement-telemetry-collection.md]
- [Source: src/services/telemetry_service.py]
- [Source: docs/telemetry.md]
- [Source: tests/unit/test_telemetry_service.py]
- [Source: tests/integration/test_telemetry_integration.py]
- [Source: tests/e2e/test_telemetry_collection_e2e.py]

## Dev Agent Record

### Agent Model Used

GPT-5 Codex
