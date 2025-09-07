type IdBase = string | { text: string };
type NextPage<T> = { hasNext: boolean; next: () => T };
interface SResultsSub<TSearchId extends IdBase>
  extends NextPage<SResultsSub<TSearchId>> {
  results: TSearchId[];
}
interface SResultsDownload<TDownloadId extends IdBase>
  extends NextPage<SResultsDownload<TDownloadId>> {
  results: TDownloadId[];
}
type SResults<TSearchId extends IdBase, TDownloadId extends IdBase> =
  | ({ page: "sub" } & SResultsSub<TSearchId>)
  | ({ page: "download" } & SResultsDownload<TDownloadId>);

type ProviderOpts = {
  searchId: IdBase;
  downloadId: IdBase;
};

type ProviderDefaultOpts = {
  searchId: string;
  downloadId: string;
};

type ResolveProviderOptions<TOverrides extends Partial<ProviderOpts>> =
  ProviderDefaultOpts & TOverrides;

type Provider<TOverrides extends Partial<ProviderOpts> = {}> =
  ResolveProviderOptions<TOverrides> extends infer TOpts
    ? TOpts extends ProviderOpts // Safety check on the inferred type
      ? SResults<TOpts["searchId"], TOpts["downloadId"]> extends infer TSRes
        ? {
            search: (query: string) => Promise<TSRes>;
            query: (query: TOpts["searchId"]) => Promise<TSRes>;
            download: (query: TOpts["downloadId"]) => Promise<void>;
          }
        : never
      : never
    : never;

export type { Provider };
