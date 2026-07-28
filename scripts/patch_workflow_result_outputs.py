"""Align workflow result outputs with BulkUpdateDeleteWebhooks conventions."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

WORKFLOWS = [
    {
        "path": REPO
        / "workflows/SyncAlertSettingsFromTemplate__definition_workflow_02X33Q15973CK5PjWvTHxVAHbN9dWwx56ix/definition_workflow_02X33Q15973CK5PjWvTHxVAHbN9dWwx56ix.json",
        "report_script_id": "definition_activity_02X33Q4IEDHYP7Uq9eA5LlgRlfhcFCcTfKF",
        "status_message_query": "overall_status",
        "result_query": "result_json",
        "report_query": "formatted_report",
        "final_store_titles": {"Set Standard Outputs"},
        "complete_if_else_titles": {"Complete Based on Report Status"},
    },
    {
        "path": REPO
        / "workflows/UpdateLocalStatusPagePassword__definition_workflow_02X3U9WW7XIJM11Zq3kk8J5oB4Eirj1Bc7g/definition_workflow_02X3U9WW7XIJM11Zq3kk8J5oB4Eirj1Bc7g.json",
        "report_script_id": "definition_activity_02X3U9Z35UNTA46AQYOvrwSRNQrUImcwHvv",
        "status_message_query": "status_message",
        "result_query": "result_json",
        "report_query": "report",
        "final_store_titles": {"Store Workflow Outputs"},
        "complete_if_else_titles": {"Complete Based on Report Status"},
    },
    {
        "path": REPO
        / "workflows/AuditOrganizationSettings__definition_workflow_02VUY2YFCSM580eSv9Mg4lACoZszdI8WA5W/definition_workflow_02VUY2YFCSM580eSv9Mg4lACoZszdI8WA5W.json",
        "report_script_id": "definition_activity_02VUY30HCUII76FEMe7wXbkRHIfIrVQL7qG",
        "status_message_query": "status_message",
        "result_query": "finalAggregatedData",
        "report_query": None,
        "final_store_titles": {"Set Final Output"},
        "complete_if_else_titles": {"Finalizing and output"},
    },
]

OUTPUT_FIELD_ORDER = [
    "Status Code",
    "Status Message",
    "Error Message",
    "Result",
    "workflow_results",
    "workflow_results_code",
    "Formatted Report",
]

RESULT_CODES = {
    200: "completed-successfully",
    207: "partially-completed",
    500: "completed-unsuccessfully",
}


def activity_id(seed: str) -> str:
    digest = hashlib.sha256(seed.encode()).hexdigest()[:26].upper()
    return f"definition_activity_02{digest}"


def build_output_paths(workflow: dict) -> dict[str, str]:
    wf_id = workflow["unique_name"]
    paths: dict[str, str] = {}
    for var in workflow.get("variables", []):
        if var.get("properties", {}).get("scope") != "output":
            continue
        paths[var["properties"]["name"]] = f"$workflow.{wf_id}.output.{var['unique_name']}$"
    paths["workflow_results"] = f"$workflow.{wf_id}.output.workflow_results$"
    paths["workflow_results_code"] = f"$workflow.{wf_id}.output.workflow_results_code$"
    return paths


def is_output_vtu(vtu: dict, wf_id: str) -> bool:
    return vtu.get("variable_to_update", "").startswith(f"$workflow.{wf_id}.output.")


def only_wf_result_code(activity: dict, wf_id: str) -> bool:
    if activity.get("type") != "core.set_multiple_variables":
        return False
    vtus = activity.get("properties", {}).get("variables_to_update") or []
    code = f"$workflow.{wf_id}.output.workflow_results_code$"
    return len(vtus) == 1 and vtus[0].get("variable_to_update") == code


def is_failure_output_activity(activity: dict, final_store_titles: set[str]) -> bool:
    if activity.get("type") != "core.set_multiple_variables":
        return False
    props = activity.get("properties", {})
    title = activity.get("title") or props.get("display_name") or ""
    if title in final_store_titles:
        return False
    blob = " ".join(
        [
            activity.get("title") or "",
            activity.get("name") or "",
            props.get("display_name") or "",
            props.get("description") or "",
        ]
    ).lower()
    return any(
        x in blob
        for x in (
            "failure",
            "validation",
            "invalid",
            "fail ",
            "get organizations failed",
            "set outputs after",
            "set invalid",
        )
    ) or activity.get("name") in ("Set Failure Outputs", "Set Invalid Mode Outputs")


def ensure_failure_wf_fields(vtus: list, paths: dict[str, str]) -> list:
    keys = {v["variable_to_update"] for v in vtus}
    if paths["workflow_results"] not in keys:
        vtus.append(
            {
                "variable_to_update": paths["workflow_results"],
                "variable_value_new": paths["Status Message"],
            }
        )
    if paths["workflow_results_code"] not in keys:
        vtus.append(
            {
                "variable_to_update": paths["workflow_results_code"],
                "variable_value_new": "workflow-errored",
            }
        )
    return vtus


def reorder_output_vtus(vtus: list, paths: dict[str, str], wf_id: str) -> list:
    order_index = {
        paths[label]: OUTPUT_FIELD_ORDER.index(label)
        for label in OUTPUT_FIELD_ORDER
        if label in paths
    }
    local = [v for v in vtus if not is_output_vtu(v, wf_id)]
    output_only = [v for v in vtus if is_output_vtu(v, wf_id)]
    output_only.sort(key=lambda v: order_index.get(v["variable_to_update"], 99))
    return local + output_only


def make_result_code_activity(wf_id: str, branch_code: int, seed: str) -> dict:
    return {
        "unique_name": activity_id(f"{wf_id}-wrc-{branch_code}-{seed}"),
        "name": "Set Variables",
        "title": "Set Workflow result code",
        "type": "core.set_multiple_variables",
        "base_type": "activity",
        "properties": {
            "continue_on_failure": False,
            "description": "Set Variables",
            "display_name": "Set Workflow result code",
            "skip_execution": False,
            "variables_to_update": [
                {
                    "variable_to_update": f"$workflow.{wf_id}.output.workflow_results_code$",
                    "variable_value_new": RESULT_CODES[branch_code],
                }
            ],
        },
        "object_type": "definition_activity",
    }


def patch_final_store(activity: dict, cfg: dict, paths: dict[str, str]) -> None:
    prefix = f"$activity.{cfg['report_script_id']}.output.script_queries."
    vtus = [
        {"variable_to_update": paths["Status Code"], "variable_value_new": prefix + "status_code$"},
        {
            "variable_to_update": paths["Status Message"],
            "variable_value_new": prefix + cfg["status_message_query"] + "$",
        },
        {"variable_to_update": paths["Error Message"], "variable_value_new": prefix + "error_message$"},
        {
            "variable_to_update": paths["Result"],
            "variable_value_new": prefix + cfg["result_query"] + "$",
        },
        {
            "variable_to_update": paths["workflow_results"],
            "variable_value_new": prefix + cfg["status_message_query"] + "$",
        },
    ]
    if cfg.get("report_query") and "Formatted Report" in paths:
        vtus.append(
            {
                "variable_to_update": paths["Formatted Report"],
                "variable_value_new": prefix + cfg["report_query"] + "$",
            }
        )
    activity["properties"]["variables_to_update"] = vtus


def patch_complete_branches(obj, wf_id: str, cfg: dict) -> None:
    if isinstance(obj, dict):
        title = obj.get("title") or obj.get("properties", {}).get("display_name")
        if obj.get("type") == "logic.if_else" and title in cfg["complete_if_else_titles"]:
            for block in obj.get("blocks") or []:
                cond = block.get("properties", {}).get("condition") or {}
                code = cond.get("right_operand")
                if code not in RESULT_CODES:
                    continue
                actions = block.setdefault("actions", [])
                if actions and only_wf_result_code(actions[0], wf_id):
                    actions[0]["properties"]["variables_to_update"][0][
                        "variable_value_new"
                    ] = RESULT_CODES[code]
                    continue
                if actions and actions[0].get("title") == "Set Workflow result code":
                    continue
                actions.insert(0, make_result_code_activity(wf_id, code, block.get("unique_name", "")))
        for v in obj.values():
            patch_complete_branches(v, wf_id, cfg)
    elif isinstance(obj, list):
        for item in obj:
            patch_complete_branches(item, wf_id, cfg)


def patch_exit_action_lists(obj, wf_id: str, paths: dict[str, str], cfg: dict) -> None:
    """Any output set in an actions list that ends with logic.completed is an exit branch."""
    if isinstance(obj, dict):
        actions = obj.get("actions")
        if isinstance(actions, list) and any(a.get("type") == "logic.completed" for a in actions):
            for act in actions:
                if act.get("type") != "core.set_multiple_variables":
                    continue
                if only_wf_result_code(act, wf_id) or act.get("title") == "Set Workflow result code":
                    continue
                title = act.get("title") or act.get("properties", {}).get("display_name") or ""
                if title in cfg["final_store_titles"]:
                    continue
                vtus = act.get("properties", {}).get("variables_to_update") or []
                if not any(is_output_vtu(v, wf_id) for v in vtus):
                    continue
                vtus = ensure_failure_wf_fields(list(vtus), paths)
                act["properties"]["variables_to_update"] = reorder_output_vtus(vtus, paths, wf_id)
        for v in obj.values():
            patch_exit_action_lists(v, wf_id, paths, cfg)
    elif isinstance(obj, list):
        for item in obj:
            patch_exit_action_lists(item, wf_id, paths, cfg)


def walk(obj, parent_list, parent_idx, wf_id: str, paths: dict, cfg: dict, remove_ids: set) -> None:
    if not isinstance(obj, dict):
        return
    if obj.get("unique_name") in remove_ids and parent_list is not None:
        parent_list.pop(parent_idx)
        return

    if obj.get("type") == "core.set_multiple_variables":
        props = obj.get("properties", {})
        vtus = props.get("variables_to_update") or []
        title = obj.get("title") or props.get("display_name") or ""
        if title in cfg["final_store_titles"]:
            patch_final_store(obj, cfg, paths)
        elif any(is_output_vtu(v, wf_id) for v in vtus):
            if is_failure_output_activity(obj, cfg["final_store_titles"]):
                vtus = ensure_failure_wf_fields(list(vtus), paths)
            props["variables_to_update"] = reorder_output_vtus(vtus, paths, wf_id)

    if isinstance(obj.get("actions"), list):
        actions = obj["actions"]
        i = 0
        while i < len(actions):
            walk(actions[i], actions, i, wf_id, paths, cfg, remove_ids)
            if i < len(actions):
                i += 1
    if isinstance(obj.get("blocks"), list):
        blocks = obj["blocks"]
        i = 0
        while i < len(blocks):
            walk(blocks[i], blocks, i, wf_id, paths, cfg, remove_ids)
            if i < len(blocks):
                i += 1
    for key, val in obj.items():
        if key in ("actions", "blocks"):
            continue
        if isinstance(val, dict):
            walk(val, None, None, wf_id, paths, cfg, remove_ids)
        elif isinstance(val, list):
            i = 0
            while i < len(val):
                if isinstance(val[i], dict):
                    walk(val[i], val, i, wf_id, paths, cfg, remove_ids)
                if i < len(val):
                    i += 1


def collect_orphan_ids(obj, wf_id: str, remove_ids: set) -> None:
    if isinstance(obj, dict):
        if only_wf_result_code(obj, wf_id) and obj.get("title") != "Set Workflow result code":
            remove_ids.add(obj["unique_name"])
        for v in obj.values():
            collect_orphan_ids(v, wf_id, remove_ids)
    elif isinstance(obj, list):
        for item in obj:
            collect_orphan_ids(item, wf_id, remove_ids)


def patch_file(cfg: dict) -> None:
    data = json.loads(cfg["path"].read_text(encoding="utf-8"))
    workflow = data["workflow"]
    wf_id = workflow["unique_name"]
    paths = build_output_paths(workflow)
    remove_ids: set[str] = set()
    collect_orphan_ids(workflow, wf_id, remove_ids)
    walk(workflow, None, None, wf_id, paths, cfg, remove_ids)
    patch_exit_action_lists(workflow, wf_id, paths, cfg)
    patch_complete_branches(workflow, wf_id, cfg)
    cfg["path"].write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Patched {cfg['path'].name}: removed {len(remove_ids)} orphan steps")


def main() -> None:
    for cfg in WORKFLOWS:
        patch_file(cfg)


if __name__ == "__main__":
    main()
