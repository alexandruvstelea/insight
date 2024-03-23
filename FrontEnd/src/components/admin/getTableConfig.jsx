import { Edit as EditIcon, Delete as DeleteIcon } from "@mui/icons-material";
import {
  Box,
  Button,
  IconButton,
  Tooltip,
  DialogTitle,
  DialogContent,
  DialogActions,
} from "@mui/material";
import { MRT_EditActionButtons } from "material-react-table";

export const defSelectColumnOption = (editSelectOptions) => ({
  editVariant: "select",
  editSelectOptions,
  muiEditTextFieldProps: {
    select: true,
  },
});

export const columnOption = (
  accessorKey,
  header,
  size,
  minSize,
  enableEditing,
  additionalOptions = {}
) => ({
  accessorKey,
  header,
  size,
  minSize,
  enableEditing,
  ...additionalOptions,
});

export const tableConfigDef = (columns, data) => ({
  columns,
  data: data || [],
  enablePagination: false,
  enableRowVirtualization: true,
  enableColumnActions: false,
  muiTableContainerProps: { sx: { maxHeight: "700px" } },
  initialState: {
    density: "compact",
    sorting: [
      {
        id: "id",
        desc: false,
      },
    ],
  },
});

export const tableConfig = (
  columns,
  data,
  tableName,
  handleCreate,
  handleSaveRoom,
  url,
  getFetch
) => ({
  ...tableConfigDef(columns, data),
  // layoutMode: 'grid-no-grow',
  positionActionsColumn: "first",
  editDisplayMode: "row",
  enableEditing: true,

  enableColumnPinning: true,
  displayColumnDefOptions: {
    "mrt-row-actions": {
      header: "Editează/Șterge",
      size: 100,
    },
  },
  renderCreateRowDialogContent: ({ table, row, internalEditComponents }) => (
    <>
      <DialogTitle variant="h4">Adaugă {tableName}</DialogTitle>
      <DialogContent
        sx={{ display: "flex", flexDirection: "column", gap: "1rem" }}
      >
        {internalEditComponents.filter(
          (component) => component.key !== "mrt-row-create_id"
        )}
      </DialogContent>
      <DialogActions>
        <MRT_EditActionButtons variant="text" table={table} row={row} />
      </DialogActions>
    </>
  ),
  onCreatingRowSave: handleCreate,
  onEditingRowSave: handleSaveRoom,
  renderTopToolbarCustomActions: ({ table }) => (
    <>
      <Button
        variant="contained"
        onClick={() => {
          table.setCreatingRow(true);
        }}
      >
        Adaugă {tableName}
      </Button>
    </>
  ),
  renderRowActions: ({ row, table }) => (
    <Box sx={{ display: "flex", gap: "1rem" }}>
      <Tooltip title="Editează">
        <IconButton onClick={() => table.setEditingRow(row)}>
          <EditIcon />
        </IconButton>
      </Tooltip>
      <Tooltip title="Șterge">
        <IconButton
          color="error"
          onClick={async () => {
            await deleteItem(url, row.original.id, getFetch);
          }}
        >
          <DeleteIcon />
        </IconButton>
      </Tooltip>
    </Box>
  ),
});

export const deleteItem = async (url, id, fetchFunction) => {
  try {
    const response = await fetch(
      `${process.env.REACT_APP_API_URL}/${url}/${id}`,
      {
        method: "DELETE",
        credentials: "include",
      }
    );
    if (!response.ok) {
      throw new Error(`Failed to delete ${url.slice(0, -1)}`);
    }
    fetchFunction();
  } catch (err) {
    console.error(`Error deleting ${url.slice(0, -1)}:`, err);
  }
};
