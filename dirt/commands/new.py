import click

from dateparser import parse

from dirt.libs import incident, log

from dirt import hooks


@click.command("new", help="Create new incident and set as current")
@click.option("--desc", help="Short description of incident (optional)")
@click.option("--created-at", help="Override creation date")
@click.option("--owner", help="Override owner name")
@click.pass_context
@hooks.hookable
def new_command(ctx, desc, created_at, owner):
    current = incident.get_current_incident()
    if not log.QUIET_MODE and current is not None and not current.closed:
        log.warning("Current incident {current} is opened.", current=current.identifier)
        if not click.confirm("Do you really want to create new incident?"):
            ctx.abort()
    created_at = created_at and parse(created_at)
    current = incident.Incident(cname=desc, created_on=created_at, owner=owner)
    current.store()
    incident.set_current_incident(current)
    log.success("New incident created {incident}", incident=current.identifier)
    ctx.obj["INCIDENT"] = current


COMMAND = new_command
