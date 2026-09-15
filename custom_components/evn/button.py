# Copyright (c) 2026 @Zeridon
# SPDX-License-Identifier: MIT

"""Buttons for the EVN Bulgaria integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EVNCoordinator

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


class EVNRefreshButton(
    CoordinatorEntity[EVNCoordinator],
    ButtonEntity,
):
    """Button to manually refresh EVN prices."""

    _attr_has_entity_name = True
    _attr_translation_key = "refresh_prices"
    _attr_icon = "mdi:web-refresh"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_unique_id = "evn_refresh_prices"

    def __init__(self, coordinator: EVNCoordinator) -> None:
        """Initialize the refresh button."""
        super().__init__(coordinator)

        self._attr_device_info = {
            "identifiers": {(DOMAIN, "evn")},
            "name": "EVN Bulgaria",
            "manufacturer": "EVN",
        }

    async def async_press(self) -> None:
        """Refresh EVN prices."""
        await self.coordinator.async_request_refresh()


class EVNRecalculateTariffButton(
    CoordinatorEntity[EVNCoordinator],
    ButtonEntity,
):
    """Button to manually recalculate the current tariff."""

    _attr_has_entity_name = True
    _attr_translation_key = "recalculate_tariff"
    _attr_icon = "mdi:timer-refresh-outline"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_unique_id = "evn_recalculate_tariff"

    def __init__(self, coordinator: EVNCoordinator) -> None:
        """Initialize the button."""
        super().__init__(coordinator)

        self._attr_device_info = {
            "identifiers": {(DOMAIN, "evn")},
            "name": "EVN Bulgaria",
            "manufacturer": "EVN",
        }

    async def async_press(self) -> None:
        """Recalculate the current tariff."""
        self.coordinator.async_recalculate_tariff()


async def async_setup_entry(
    _hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EVN buttons."""
    coordinator: EVNCoordinator = entry.runtime_data

    async_add_entities(
        [
            EVNRefreshButton(coordinator),
            EVNRecalculateTariffButton(coordinator),
        ]
    )
