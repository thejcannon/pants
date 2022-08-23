# Copyright 2019 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import annotations

from pants.base.specs import Specs
from pants.engine.console import Console
from pants.engine.fs import (
    Workspace,
)
from pants.engine.internals.build_files import BuildFileOptions
from pants.engine.rules import Get, collect_rules, goal_rule, rule
from pants.engine.unions import UnionMembership, union


from pants.core.goals._change_files_utils import (
    _change_target_sources_batch,
    _change_build_files_batch,
    _change_files_goal,
    ChangeTargetSourcesBatchRequest,
    ChangeBuildFilesBatchRequest,
    ChangeFilesSubsystemBase,
    _ChangeTargetSourcesRequest,
    ChangeFilesGoalBase,
    _ChangeBuildFilesRequest,
    ChangedFilesResult,
    ChangedFilesBatchResult,
)


@union
class FmtTargetsRequest(_ChangeTargetSourcesRequest):
    pass


@union
# Prefixed with `_` because we aren't sure if this union will stick long-term, or be subsumed when
# we implement https://github.com/pantsbuild/pants/issues/16480.
class _FmtBuildFilesRequest(_ChangeBuildFilesRequest):
    pass


class FmtSubsystem(ChangeFilesSubsystemBase):
    name = "fmt"
    help = "@TODO..."

    @classmethod
    def activated(cls, union_membership: UnionMembership) -> bool:
        return FmtTargetsRequest in union_membership


class _FmtBuildFilesBatchRequest(ChangeBuildFilesBatchRequest):
    pass


class _FmtTargetBatchRequest(ChangeTargetSourcesBatchRequest):
    pass


class Fmt(ChangeFilesGoalBase):
    subsystem_cls = FmtSubsystem


@goal_rule
async def fmt(
    console: Console,
    specs: Specs,
    fmt_subsystem: FmtSubsystem,
    build_file_options: BuildFileOptions,
    workspace: Workspace,
    union_membership: UnionMembership,
) -> Fmt:
    return await _change_files_goal(
        goal_cls=Fmt,
        console=console,
        specs=specs,
        goal_subsystem=fmt_subsystem,
        build_file_options=build_file_options,
        workspace=workspace,
        union_membership=union_membership,
        get_target_batch_results_get=lambda request_types, batch: Get(
            ChangedFilesBatchResult,
            _FmtTargetBatchRequest(request_types, batch),
        ),
        get_build_files_batch_results_get=lambda request_types, batch: Get(
            ChangedFilesBatchResult,
            _FmtBuildFilesBatchRequest(request_types, tuple(batch)),
        ),
    )


@rule
async def fmt_build_files_batch(
    request: _FmtBuildFilesBatchRequest,
) -> ChangedFilesBatchResult:
    return await _change_build_files_batch(
        request,
        get_result_get=lambda request: Get(ChangedFilesResult, _FmtBuildFilesRequest, request),
    )


@rule
async def fmt_target_batch(
    request: _FmtTargetBatchRequest,
) -> ChangedFilesBatchResult:
    return await _change_target_sources_batch(
        request,
        get_result_get=lambda request: Get(ChangedFilesResult, FmtTargetsRequest, request),
    )


def rules():
    return collect_rules()
