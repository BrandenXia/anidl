type IdBase = string | { text: string };
// not using this because interface cannot extend union types
// type NextPage<T> =
//   | { hasNext: true; next: () => Promise<T> }
//   | { hasNext: false; next?: undefined };
type NextPage<T> = { hasNext: boolean; next?: () => Promise<T> };

interface SResultsSub<TSearchId extends IdBase>
  extends NextPage<SResultsSub<TSearchId>> {
  page: "sub";
  results: TSearchId[];
}
interface SResultsDownload<TDownloadId extends IdBase>
  extends NextPage<SResultsDownload<TDownloadId>> {
  page: "download";
  results: TDownloadId[];
}
type SResults<TSearchId extends IdBase, TDownloadId extends IdBase> =
  | SResultsSub<TSearchId>
  | SResultsDownload<TDownloadId>;

type ProviderOpts = {
  searchId: IdBase;
  downloadId: IdBase;
};

type ProviderDefaultOpts = {
  searchId: string;
  downloadId: string;
};

type ResolveProviderOptions<TOverrides extends Partial<ProviderOpts>> = Omit<
  ProviderDefaultOpts,
  keyof TOverrides
> &
  TOverrides;

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

export type { Provider, SResults, SResultsSub, SResultsDownload };
