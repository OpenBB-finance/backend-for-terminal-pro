import { cors } from "@elysiajs/cors";
import { Elysia } from "elysia";
import { Logestic } from "logestic";

const widgets = {
	protocols: {
		name: "Protocols",
		description: "List all protocols on defillama along with their tvl",
		endpoint: "/protocols",
	},
	cabonds: {
		name: "Bonds CA",
		description: "Bonds from Canada",
		endpoint: "/ca-bonds",
		enableSSRM: true,
		data: {
			table: {
				columnsDefs: [
					{
						field: "secKey",
						headerName: "Security Key",
						sortable: true,
						filter: true,
					},
					{
						field: "issuer",
						headerName: "Issuer",
						sortable: true,
						filter: true,
					},
					{
						field: "securityId",
						headerName: "Security ID",
						sortable: true,
						filter: true,
					},
					{ field: "cusip", headerName: "CUSIP", sortable: true, filter: true },
					{ field: "isin", headerName: "ISIN", sortable: true, filter: true },
					{ field: "figi", headerName: "FIGI", sortable: true, filter: true },
					{
						field: "maturityDate",
						headerName: "Maturity Date",
						sortable: true,
						filter: true,
					},
					{
						field: "couponRate",
						headerName: "Coupon Rate",
						sortable: true,
						filter: true,
					},
					{
						field: "lastPrice",
						headerName: "Last Price",
						sortable: true,
						filter: true,
					},
					{
						field: "lastYield",
						headerName: "Last Yield",
						sortable: true,
						filter: true,
					},
					{
						field: "totalTrades",
						headerName: "Total Trades",
						sortable: true,
						filter: true,
					},
					{
						field: "lastTradedDate",
						headerName: "Last Traded Date",
						sortable: true,
						filter: true,
					},
					{
						field: "highestPrice",
						headerName: "Highest Price",
						sortable: true,
						filter: true,
					},
					{
						field: "lowestPrice",
						headerName: "Lowest Price",
						sortable: true,
						filter: true,
					},
					{
						field: "bondType",
						headerName: "Bond Type",
						sortable: true,
						filter: true,
					},
					{
						field: "originalIssueDate",
						headerName: "Original Issue Date",
						sortable: true,
						filter: true,
					},
				],
			},
		},
	},
};

async function readBondsData() {
	const path = "./ca-bonds.json";
	const file = Bun.file(path);
	return await file.json();
}

async function fetchProtocols() {
	try {
		const response = await fetch("https://api.llama.fi/protocols");
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		return await response.json();
	} catch (error) {
		console.error("Error fetching protocols:", error);
		throw error;
	}
}

const app = new Elysia()
	.use(Logestic.preset("common"))
	.use(cors())
	.get("/", () => "Hello, World!")
	.get("/widgets.json", () => Response.json(widgets))
	.get("/protocols", async () => {
		try {
			const protocols = await fetchProtocols();
			return Response.json(protocols);
		} catch (error) {
			return new Response("Error fetching protocols", { status: 500 });
		}
	})
	.post("/ca-bonds", async ({ body }) => {
		try {
			const bondsData = await readBondsData();
			const { startRow, endRow, sortModel, filterModel } = body as {
				startRow: number;
				endRow: number;
				sortModel?: { colId: string; sort: "asc" | "desc" }[];
				filterModel?: Record<string, { type: string; filter: string }>;
			};

			// Apply sorting
			if (sortModel && sortModel.length > 0) {
				const { colId, sort } = sortModel[0];
				bondsData.sort((a: any, b: any) => {
					if (a[colId] < b[colId]) return sort === "asc" ? -1 : 1;
					if (a[colId] > b[colId]) return sort === "asc" ? 1 : -1;
					return 0;
				});
			}

			// Apply filtering
			let filteredData = bondsData;
			if (filterModel) {
				for (const key of Object.keys(filterModel)) {
					const { type, filter } = filterModel[key];
					filteredData = filteredData.filter((item: any) => {
						if (type === "contains") {
							return item[key].toLowerCase().includes(filter.toLowerCase());
						}
						return true;
					});
				}
			}

			// Apply pagination
			const paginatedData = filteredData.slice(startRow, endRow);

			return {
				rows: paginatedData,
				lastRow: filteredData.length,
			};
		} catch (error) {
			return new Response("Error processing request", { status: 500 });
		}
	})
	.listen(3000);

console.log(
	`🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`,
);
