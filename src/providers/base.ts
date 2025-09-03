type OnlyLiteralKeys<T> = string extends keyof T ? never : T;

type ProviderOpts = {
  AnimeID: unknown;
  EpID: unknown;
  SearchOpts: object;
  EpOpts: object;
  DownloadOpts: object;
};

type ProviderDefaultOpts = {
  AnimeID: string;
  EpID: string;
  SearchOpts: {};
  EpOpts: {};
  DownloadOpts: {};
};

type ResolveProviderOptions<TOverrides extends Partial<ProviderOpts>> =
  ProviderDefaultOpts & TOverrides;

type BaseCacheOpts =
  | boolean
  | {
      /** maxAge is in seconds */
      maxAge: number;
    };
type CacheOpts =
  | BaseCacheOpts
  | {
      search?: BaseCacheOpts;
      getEps?: BaseCacheOpts;
      download?: BaseCacheOpts;
    };

type Provider<TOverrides extends Partial<ProviderOpts> = {}> =
  ResolveProviderOptions<TOverrides> extends infer TOpts
    ? TOpts extends ProviderOpts // Safety check on the inferred type
      ? {
          cache?: CacheOpts;
          search: (
            query: string,
            opts?: OnlyLiteralKeys<TOpts["SearchOpts"]>,
          ) => Promise<Record<string, TOpts["AnimeID"]>>;
          getEps: (
            id: TOpts["AnimeID"],
            opts?: OnlyLiteralKeys<TOpts["EpOpts"]>,
          ) => Promise<Record<string, TOpts["EpID"]>>;
          download: (
            animeId: TOpts["AnimeID"],
            epId: TOpts["EpID"],
            opts?: OnlyLiteralKeys<TOpts["DownloadOpts"]>,
          ) => Promise<void>;
        }
      : never
    : never;

export type { Provider };
